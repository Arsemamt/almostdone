from django.shortcuts import render,redirect,get_object_or_404
from .models import Home,Contact,Course,QuesModel,About,ExerciseResult
from .forms import addQuestionform, ContactForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from random import sample
from datetime import datetime
from django.utils import timezone

def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
             messages.error(request,'User does not exist.')
            
        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or Password does not exist.')

    context={'page':page}
    return render(request,'login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration.')

    context = {'form': form}
    return render(request,'login_register.html',context)
 

@login_required(login_url='login')
def home(request):
    homepage = Home.objects.all()
    recent_courses = Course.objects.order_by('-id')[:3]
    recent_results = ExerciseResult.objects.filter(user=request.user).order_by('-created_at')[:10]
    correct_count = sum(1 for result in recent_results if result.correct)

    context = {'homepage': homepage,'recent_courses': recent_courses,'recent_results': recent_results,'correct_count':correct_count}
    return render(request,'index.html', context)

def about(request):
    about_page = About.objects.all()
    context={'about_page':about_page}
    return render(request,'about.html',context)

@login_required(login_url='login')
def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            contact_info = Contact.objects.create(name=name, email=email, message=message)
            messages.success(request, "Form submitted successfully!")
            return redirect('contact_form')
    else:
        form = ContactForm()
        messages.info(request, "Please use the form to submit your message.")
    return render(request, 'contact.html', {'form': form})





def courses_list(request):
    search_query = request.GET.get('search_query')
    courses = Course.objects.all()

    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    paginator = Paginator(courses, 8)  # Show 8 courses per page
    page_number = request.GET.get('page')
    try:
        courses = paginator.page(page_number)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    context = {'courses': courses}
    return render(request,'courses.html', context)

# Create your views here.

@login_required(login_url='login')
def exercise(request):
    if request.method == 'POST':
        questions = QuesModel.objects.all()
        score = 0
        wrong = 0
        correct = 0
        total = 0
        wrong_answers = []

        for q in questions:
            total += 1
            selected_answer = request.POST.get(str(q.id))
            print("Selected Answer:", selected_answer)
            print("Correct Answer:", q.ans)
            print()

            if selected_answer and q.ans:
                selected_answer = selected_answer.strip().upper()
                correct_answer = q.ans.strip().upper()

                if selected_answer == correct_answer:
                    score += 10
                    correct += 1
                else:
                    wrong += 1
                    wrong_answers.append(q)

                ExerciseResult.objects.create(
                    user=request.user,
                    score=score,
                    selected_answer=selected_answer,  # Set the selected answer
                    correct=selected_answer == correct_answer,
                )
            else:
                print("Error: Selected answer or correct answer missing")

        percent = score / (total * 10) * 100
        print("Score:", score)
        print("Percentage:", percent)

        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total,
            'questions': wrong_answers
        }
        return render(request, 'result.html', context)
    else:
        all_questions = QuesModel.objects.all()
        random_questions = sample(list(all_questions),min(len(all_questions),10))
        context = {'questions': random_questions}
        return render(request, 'exercise.html', context)




@login_required(login_url='login')
def addQuestion(request):
    form = addQuestionform()

    allowed_username = 'asdf'

    allowed_user = User.objects.get(username=allowed_username)

    if request.user!= allowed_user:
        return redirect('exercise')

    if request.method == 'POST':
        form = addQuestionform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exercise')
    context = {'form': form}
    return render(request, 'addQuestion.html', context)



def course_view(request):
    search_query = request.GET.get('search_query')
    courses = Course.objects.all()

    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    paginator = Paginator(courses, 8)
    page_number = request.GET.get('page')
    try:
        courses = paginator.page(page_number)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    context = {'courses': courses,'search_query':search_query}
    return render(request, 'courses.html', context)


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    related_courses = Course.objects.exclude(pk=course_id).filter(
        Q(title__icontains=course.title) |
        Q(title__icontains=course.title.split()[0])
    )[:3] 
    print(related_courses)
    return render(request, 'course_detail.html', {'course': course, 'related_courses': related_courses})

def search_courses(request):
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(title__icontains=query) | Course.objects.filter(description__icontains=query)
    else:
        courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses, 'query': query})


# def course_view(request):
    course_view = request.GET.get('query', '')
    context = {'course_view': course_view}
    return render(request, 'courses.html', context)



