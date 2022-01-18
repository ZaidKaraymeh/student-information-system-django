from django import forms
# from django.forms import ChoiceWidget

from users.models import CustomUser, Course, Post, Assignment, AssignmentSubmission, Quiz, MultipleChoiceQuestion, AttendanceReport
from django.contrib.auth.forms import UserCreationForm

# from .models import Profile

class AddCourseForm(forms.ModelForm):
    class Meta:
        # Interacts with User model
        model = Course
        # What fields to show and in which order
        fields = ["name", "code", "section", "instructor"]
        
    def __init__(self, *args, **kwargs):
        super(AddCourseForm  , self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['code'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['section'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['instructor'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['code'].widget.attrs['class'] = 'form-control'
        self.fields['section'].widget.attrs['class'] = 'form-control'
        self.fields['instructor'].widget.attrs['class'] = 'form-control'

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
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',}))

    class Meta:
        # Interacts with User model
        model = CustomUser
        # What fields to show and in which order
        fields = ["first_name", "last_name", "email", "phone_number",  "password1", "password2", "year", "address"]
        widgets = {
                'first_name': forms.TextInput(attrs={'class': 'form-control',}), 
                'last_name': forms.TextInput(attrs={'class': 'form-control',}), 
                'address': forms.TextInput(attrs={'class': 'form-control',}), 
                'phone_number': forms.TextInput(attrs={'class': 'form-control',}), 
                'password1': forms.TextInput(attrs={'class': 'form-control',}), 
                'password2': forms.TextInput(attrs={'class': 'form-control',}), 
            }
    def __init__(self, *args, **kwargs):
        super(AddStudentForm  , self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
        self.fields['first_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['last_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['email'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['phone_number'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['address'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['year'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['password1'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['password2'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['year'].widget.attrs['class'] = 'form-control'
class AddStaffForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',}))
    
    def __init__(self, *args, **kwargs):
        super(AddStaffForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
    class Meta:
        # Interacts with User model
        model = CustomUser
        # What fields to show and in which order
        fields = ["first_name", "last_name", "email", "phone_number",  "password1", "password2", "year", "address"]


        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control',}), 
            'last_name': forms.TextInput(attrs={'class': 'form-control',}), 
            'address': forms.TextInput(attrs={'class': 'form-control',}), 
            'phone_number': forms.TextInput(attrs={'class': 'form-control',}), 
            'password1': forms.TextInput(attrs={'class': 'form-control',}), 
            'password2': forms.TextInput(attrs={'class': 'form-control',}), 
        }
    def __init__(self, *args, **kwargs):
        super(AddStaffForm  , self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
        self.fields['first_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['last_name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['email'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['phone_number'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['address'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['year'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['password1'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['password2'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['year'].widget.attrs['class'] = 'form-control'
        # self.fields['first_name'].label = ""
        # self.fields['last_name'].label = ""
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
            'title': forms.TextInput(attrs={'class': 'form-control',}), 
            'content': forms.Textarea(attrs={'class': 'form-control',}),
        }
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['title'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['title'].label = ""
        self.fields['content'].label = ""

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
    file = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes',
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )
    class Meta:
        model = Assignment

        fields = ['name', 'description', 'category', 'possible_points', 'courses', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}) ,
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(AssignmentForm  , self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['description'].widget.attrs['style'] = 'width:100%; height:300px;'
        self.fields['category'].widget.attrs['style'] = 'width:100%; height:40px; font-weight: bold'
        self.fields['courses'].widget.attrs['style'] = 'width:100%; height:40px;font-weight: bold'
        self.fields['possible_points'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['courses'].widget.attrs['class'] = 'form-control'
        self.fields['possible_points'].widget.attrs['class'] = 'form-control'

class AssignmentSubmissionForm(forms.ModelForm):
    file = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes',
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )
    class Meta:
        model = AssignmentSubmission

        fields = ['file']
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}) ,
        #     'description': forms.Textarea(attrs={'class': 'form-control'}),
        # }
    # def __init__(self, *args, **kwargs):
    #     super(AssignmentForm  , self).__init__(*args, **kwargs)

    #     self.fields['name'].widget.attrs['style'] = 'width:100%; height:40px;'
    #     self.fields['description'].widget.attrs['style'] = 'width:100%; height:300px;'
    #     self.fields['category'].widget.attrs['style'] = 'width:100%; height:40px; font-weight: bold'
    #     self.fields['courses'].widget.attrs['style'] = 'width:100%; height:40px;font-weight: bold'
    #     self.fields['possible_points'].widget.attrs['style'] = 'width:100%; height:40px;'
    #     self.fields['name'].widget.attrs['class'] = 'form-control'
    #     self.fields['description'].widget.attrs['class'] = 'form-control'
    #     self.fields['category'].widget.attrs['class'] = 'form-control'
    #     self.fields['courses'].widget.attrs['class'] = 'form-control'
    #     self.fields['possible_points'].widget.attrs['class'] = 'form-control'

    
# class AttendanceForm(forms.ModelForm):
#     class Meta:
#         model = Attendance
#         fields = ["note"]


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

class AttendanceReportForm(forms.ModelForm):
    class Meta:
        model = AttendanceReport
        fields = ['student', 'is_absent', 'note', 'instructor']
        exclude = ['course']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
           'is_absent': "",
           'note': "",
           'instructor': "",
           'course': "",
           'student': "",
       }
    def __init__(self, *args, **kwargs):
        super(AttendanceReportForm  , self).__init__(*args, **kwargs)

        self.fields['is_absent'].required = False
        self.fields['note'].required = False

        self.fields['student'].widget.attrs['style'] = 'width:100%; height:40px; border:none; background:transparent; pointer-events: none; -webkit-appearance: none;'
        self.fields['instructor'].widget.attrs['style'] = 'width:100%; height:40px; border:none; background:transparent; pointer-events: none; -webkit-appearance: none;'
        self.fields['note'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['student'].widget.attrs['class'] = 'form-control text-center'
        self.fields['instructor'].widget.attrs['class'] = 'form-control text-center'
        self.fields['note'].widget.attrs['class'] = 'form-control'
    field_order = ['student', 'is_absent', 'note']


