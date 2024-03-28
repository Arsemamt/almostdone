from  django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class addQuestionform(forms.ModelForm):
    class Meta:
        model = QuesModel
        fields = "__all__"


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea, label='Message')
