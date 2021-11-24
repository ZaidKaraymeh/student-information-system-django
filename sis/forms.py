from django import forms

from users.models import CustomUser, Course
from django.contrib.auth.forms import UserCreationForm

# from .models import Profile

class AddCourseForm(forms.ModelForm):
    class Meta:
        # Interacts with User model
        model = Course
        # What fields to show and in which order
        fields = ["name", "code", "section", "instructor"]

class AddStudentForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        # Interacts with User model
        model = CustomUser
        # What fields to show and in which order
        fields = ["first_name", "last_name", "email", "password1", "password2", "year", "address"]