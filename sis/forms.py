from django import forms
# from django.forms import ChoiceWidget

from users.models import CustomUser, Course, Post, Attendance, Assignment, Quiz, MultipleChoiceQuestion
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
            ) for course in Course.objects.all().order_by('code')
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
    
    def __init__(self, *args, **kwargs):
        super(AddStudentForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        # Interacts with User model
        model = CustomUser
        # What fields to show and in which order
        fields = ["first_name", "last_name", "email", "phone_number",  "password1", "password2", "year", "address"]
class AddStaffForm(UserCreationForm):
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        super(AddStaffForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
    class Meta:
        # Interacts with User model
        model = CustomUser
        # What fields to show and in which order
        fields = ["first_name", "last_name", "email", "phone_number",  "password1", "password2", "year", "address"]

    def __init__(self, *args, **kwargs):
        super(AddStaffForm  , self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

# For course posts
class PostForm(forms.ModelForm):
    # docfile = forms.FileField(
    #     label='Select a file',
    #     help_text='max. 42 megabytes'
    # )

    class Meta:
        model = Post

        fields = ['title', 'content',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',}) 
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
class AssignmentForm(forms.ModelForm):
    # docfile = forms.FileField(
    #     label='Select a file',
    #     help_text='max. 42 megabytes'
    # )
    COURSE_CHOICES = [
        (
            course.id ,
            f"{course.code} {course.name} Sec {course.section}"
            ) for course in Course.objects.all().order_by('code')
    ]
    courses = forms.ChoiceField(choices=COURSE_CHOICES, label='Course')

    class Meta:
        model = Assignment

        fields = ['name', 'description', 'category', 'possible_points', 'courses']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}) ,
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["note"]


class AddMultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ['content']


class AddTestForm(forms.ModelForm):
   class Meta:
       model = Quiz
       fields = ['name', 'description']

       labels = {
           'name': "Title",
           'description': 'Description'
       }
