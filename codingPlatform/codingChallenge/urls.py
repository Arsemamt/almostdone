from django.urls import path
from .views import contact_form, home, courses_list, addQuestion, exercise, about, course_detail, search_courses, course_view, loginPage,logoutUser,registerPage
urlpatterns = [
    path('login/',loginPage,name="login"),
    path('logout/',logoutUser,name="logout"),
    path('register/',registerPage,name="register"),

    path('', home, name='home'),
    path('courses/', courses_list, name='courses'),
    path('course_view/',course_view,name='course_view'),
    path('courses/<int:course_id>/', course_detail, name='course_detail'),
    path('exercise/', exercise, name='exercise'),
    path('addQuestion/', addQuestion, name='addQuestion'),
    path('contact/', contact_form, name='contact_form'),
    path('about/', about, name='about'),
    path('search/', search_courses, name='search_courses'),
]
