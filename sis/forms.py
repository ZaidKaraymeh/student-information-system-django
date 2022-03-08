from cProfile import label
from email.policy import default
from django import forms
# from django.forms import ChoiceWidget

from users.models import CustomUser, Course, Post, Assignment, AssignmentSubmission, Quiz, MultipleChoiceQuestion, AttendanceReport, Message, Reply, Grade
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets                                       

# from .models import Profile

class AddCourseForm(forms.ModelForm):
    class Meta:
        # Interacts with User model
        model = Course
        # What fields to show and in which order
        fields = ["name", "code", "year", "section", "instructor"]
        
    def __init__(self, *args, **kwargs):
        super(AddCourseForm  , self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['code'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['year'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['section'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['instructor'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['code'].widget.attrs['class'] = 'form-control'
        self.fields['year'].widget.attrs['class'] = 'form-control'
        self.fields['section'].widget.attrs['class'] = 'form-control'
        self.fields['instructor'].widget.attrs['class'] = 'form-control'
def get_student_courses():
    COURSE_CHOICES = [
        (
            course.id ,
            f"{course.code} {course.name} Sec {course.section} {course.year}"
            ) for course in Course.objects.all().order_by('code')
    ]
    return COURSE_CHOICES
class AddStudentToCourseForm(forms.Form):
    courses = forms.ChoiceField(choices=get_student_courses, label="")
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
        fields = ["first_name", "last_name", "email", "phone_number",  "password1", "password2", "address"]


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
        self.fields['password1'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['password2'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
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
def get_courses():
    COURSE_CHOICES = [
        (
            course.id ,
            f"{course.code} {course.name} Sec {course.section} {course.year}"
            ) for course in Course.objects.all().order_by('code')
    ]
    return COURSE_CHOICES
class AssignmentForm(forms.ModelForm):
    def __init__(self, choices=[], *args, **kwargs):
        super(AssignmentForm  , self).__init__(*args, **kwargs)
        self.fields['courses'].choices = choices


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
    # docfile = forms.FileField(
    #     label='Select a file',
    #     help_text='max. 42 megabytes'
    # )
    
    # COURSE_CHOICES = Course.objects.all()
    courses = forms.ChoiceField(choices=get_courses, label='Course')
    file = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes',
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )
    class Meta:
        model = Assignment

        fields = ['name', 'description', 'category', 'possible_points', 'courses', 'file', "due_date"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}) ,
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }
        labels = {
            'due_date': 'Due Date'
        }

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

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['point_grade']
        # widgets = {
        #     'note': forms.Textarea(attrs={'class': 'form-control'}),
        # }
        labels = {
           'point_grade': "",
       }
    def __init__(self, *args, **kwargs):
        super(GradeForm  , self).__init__(*args, **kwargs)

        self.fields['point_grade'].required = False
        self.fields['point_grade'].widget.attrs['style'] = 'width:25%; height:30px;'
        self.fields['point_grade'].widget.attrs['class'] = 'form-control text-center'
    # field_order = ['student', 'is_absent', 'note']


class MessageForm(forms.ModelForm):
    file = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes',
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )
    USER_CHOICES = [
        (
            user.id ,
            f"{user.username}"
            ) for user in CustomUser.objects.all()
    ]
    users = forms.ChoiceField(choices=USER_CHOICES, label="")

    class Meta:
        model = Message

        fields = ['users','title', 'content', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Subject"}), 
            'content': forms.Textarea(attrs={'class': 'form-control','placeholder': "Enter text here..."}),
        }
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['title'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['title'].label = ""
        self.fields['content'].label = ""
        
class MessageReplyForm(forms.ModelForm):
    file = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes',
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )
    class Meta:
        model = Reply

        fields = ['title', 'content', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Subject"}), 
            'content': forms.Textarea(attrs={'class': 'form-control','placeholder': "Enter text here..."}),
        }
    def __init__(self, *args, **kwargs):
        super(MessageReplyForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['title'].widget.attrs['style'] = 'width:100%; height:40px;'
        self.fields['title'].label = ""
        self.fields['content'].label = ""
        
class MessageRecieversForm(forms.ModelForm):
    # docfile = forms.FileField(
    #     label='Select a file',
    #     help_text='max. 42 megabytes'
    # )
    is_reciever = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser

        fields = ['is_reciever']
        widgets = {
            # 'username': forms.TextInput(attrs={'class': 'form-control',}), 
        }
    def __init__(self, *args, **kwargs):
        super(MessageRecieversForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        # self.fields['username'].widget.attrs['style'] = 'width:100%; height:40px;'
        # self.fields['username'].label = ""
        self.fields['is_reciever'].label = ""
