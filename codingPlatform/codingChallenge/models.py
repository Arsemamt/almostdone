from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Home(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField()

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = "Home"

class About(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField()
    OurStory_title = models.CharField(max_length=100)
    OurStory_content = models.TextField()
    OurMission_title = models.CharField(max_length=100)
    OurMission_content = models.TextField()
    OurVision_title = models.CharField(max_length=100)
    OurVision_content = models.TextField()
    TeamMember_name = models.CharField(max_length=100)
    TeamMember_position = models.CharField(max_length=100)
    TeamMember_position1 = models.CharField(max_length=100)
    ContactAbout_title = models.CharField(max_length=100)
    ContactAbout_content = models.TextField()
    ContactAbout_email = models.EmailField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "About"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'{self.name} - {self.email}'
    
    class Meta:
        verbose_name_plural = "Contact"

class Course(models.Model):
    image = models.ImageField(null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(max_length=200,null=True)
    
    def __str__(self) -> str:
        return self.title



# Create your models here.
class QuesModel(models.Model):
    question = models.CharField(max_length=200)
    op1 = models.CharField(max_length=200)
    op2 = models.CharField(max_length=200)
    op3 = models.CharField(max_length=200)
    op4 = models.CharField(max_length=200)
    ans = models.CharField(max_length=200)
    
    def __str__(self):
        return self.question
    

class ExerciseResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    selected_answer = models.CharField(max_length=200,null=True)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Exercise Result - Score: {self.score}"
