from django import forms
# from django.forms import ChoiceWidget

from users.models import CustomUser, Course
from django.contrib.auth.forms import UserCreationForm

# from .models import Profile

class AddCourseForm(forms.ModelForm):
    class Meta:
        # Interacts with User model
        model = Course
        # What fields to show and in which order
        fields = ["name", "code", "section", "instructor"]

class AddStudentToCourseForm(forms.Form):
    COURSE_CHOICES = [
        (
            course.id ,
            f"{course.code} {course.name} Sec {course.section}"
            ) for course in Course.objects.all()
    ]
    courses = forms.ChoiceField(choices=COURSE_CHOICES)
    # class Meta:
    #     # Interacts with User model
    #     model = Course
    #     # What fields to show and in which order
    #     # fields = ["name"]
    #     exclude = ["name", "instructor", ]


class AddStudentForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        # Interacts with User model
        model = CustomUser
        # What fields to show and in which order
        fields = ["first_name", "last_name", "email", "password1", "password2", "year", "address"]