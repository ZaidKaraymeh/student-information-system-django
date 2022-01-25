from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToManyField
import os
# Create your models here.

class CustomUser(User):
    twentyTwentyone = "2020/2021"
    twentyoneTwentytwo = "2021/2022"
    twentytwoTwentythree = "2022/2023"
    UNKOWN = "UNKOWN"

    YEAR_CHOICES = [
        (twentyTwentyone, '2020/2021'),
        (twentyoneTwentytwo, '2021/2022'),
        (twentytwoTwentythree, '2022/2023'),
        (UNKOWN, "Unknown"),
    ]

    STUDENT = 'STU'
    STAFF = 'STA'
    ADMIN = "ADM"

    USER_TYPE_CHOICES = [
        (STUDENT, "Student"),
        (STAFF, "Staff"),
        (ADMIN, "Admin"),
    ]

    phone_number = models.CharField(max_length=20, null=True)
    address = models.CharField(null=True, max_length=500)
    year = models.CharField(
        max_length=10,
        choices=YEAR_CHOICES,
        default=UNKOWN
    )
    user_type = models.CharField(
        max_length=8,
        choices=USER_TYPE_CHOICES,
        default=STUDENT,

    )



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default="default.png", upload_to = "profile_pics", editable = True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

class Course(models.Model):
    name = models.CharField(null = True, max_length=50)
    code = models.CharField(null = True, max_length=8)
    section = models.CharField(default="None", max_length=15)
    instructor = models.ForeignKey(CustomUser, related_name="instructor", on_delete=models.CASCADE)
    students = models.ManyToManyField(CustomUser)
    # assignments = models.ManyToManyField(Assignment)

class Grade(models.Model):

    A = 'A'
    A_MINUS = 'A-'
    B = 'B'
    B_MINUS = 'B-'
    C = 'C'
    C_MINUS = 'C-'
    D = 'D'
    D_MINUS = 'D-'
    F = 'F'

    GRADE_TYPE_CHOICES = [
        (A, "A"),
        (A_MINUS, "A-"),
        (B, "B"),
        (B_MINUS, "B-"),
        (C, "C"),
        (C_MINUS, "C-"),
        (D, "D"),
        (D_MINUS, "D-"),
        (F, "F"),
    ]

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    letter_grade = models.CharField(
        max_length=50,
        choices=GRADE_TYPE_CHOICES,
        default=F,
        null=True,
        )
    point_grade = models.IntegerField(default=0)
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        null=True
    )

class AssignmentSubmissionFile(models.Model):
    files = models.FileField(upload_to='documents/%Y/%m/%d', null = True)
    student = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='student_submission_files'
    )
class AssignmentFile(models.Model):
    file = models.FileField(upload_to='documents/%Y/%m/%d', null = True)
    instructor = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='instructor_submission_files'
    )

    def __str__(self):
        return os.path.basename(self.file.name)
    
    def filename(self):
        return os.path.basename(self.file.name)



class AssignmentSubmission(models.Model):
    submitted_at = models.DateField(auto_now=False, auto_now_add=False)
    submitted = models.BooleanField(default=False)
    instructor = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='student_submission'
    )

    files = models.ManyToManyField(AssignmentSubmissionFile)
    description = models.CharField(max_length=9000)
    
    grade = models.ForeignKey(
        Grade, 
        on_delete=models.CASCADE,
    )

class Assignment(models.Model):
    TEST = "Test"
    QUIZ = "Quiz"
    HOMEWORK = "Homework"
    PROJECT = "Project"
    TASK = "Task"

    CATEGORY_CHOICES = [
        (TEST, "Test"),
        (QUIZ, "Quiz"),
        (HOMEWORK, "Homework"),
        (PROJECT, "Project"),
        (TASK, "Task"),
    ]

    name = models.CharField(null=True, max_length=200)
    instructor = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, 
        related_name="course", 
        on_delete=models.CASCADE
    )
    date_posted = models.DateTimeField( auto_now=False, auto_now_add=True, null=True)

    description = models.CharField(max_length=9000)
    due_date = models.DateTimeField(null=True, auto_now=False, auto_now_add=False)
    category = models.CharField(
        choices=CATEGORY_CHOICES, 
        max_length=50,
        default= TASK
    )

    student_submissions = models.ManyToManyField(AssignmentSubmission)

    possible_points = models.IntegerField()
    students_grades = models.ManyToManyField(Grade, related_name="grades")
    files = models.ManyToManyField(AssignmentFile)

    def __str__(self):
        return str(self.date_posted)

# class AssignmentFile(models.Model):
#     assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='assignment')
#     def filename(self):
#         return os.path.basename(self.file.name)

class AttendanceReport(models.Model):
    attendance_date = models.DateField(auto_now=True)
    note = models.TextField(null = True, max_length=500, default="")
    instructor = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, null=True, related_name="student", on_delete=models.CASCADE)
    is_absent = models.BooleanField()
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.instructor.username} {self.attendance_date}"
    
class Attendance(models.Model):
    date_now = models.DateField(auto_now=True, auto_now_add=False)
    attendance_reports = models.ManyToManyField(AttendanceReport)

    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    instructor = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.instructor.username} {self.date_now}"



class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    title = models.CharField( max_length=200)
    date_posted = models.DateTimeField( auto_now=False, auto_now_add=True)
    content = models.TextField(max_length=5000)
    docfile = models.FileField(upload_to='documents')
    # replies = models.ManyToManyField(CustomUser)

    def __str__(self):
        return str(self.date_posted)

    # def __str__(self):
        # return f"{self.user.username} {self.course.name} {self.title}"
    
class Quiz(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)    
    number_of_questions = models.IntegerField(default=1)
    time = models.IntegerField(help_text="Duration of the quiz in seconds", default="1")
    quiz_type = models.CharField(null=True, max_length=50)
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def get_questions(self):
        return self.multiplechoicequestion_set.all()

class MultipleChoiceQuestion(models.Model):
    content = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content
    
    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    content = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"question: {self.question.content}, answer: {self.content}, correct: {self.correct}"
    
class Marks_Of_User(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    
    def __str__(self):
        return str(self.quiz)