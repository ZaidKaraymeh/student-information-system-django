from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToManyField

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
    description = models.CharField(max_length=9000)
    due_date = models.DateTimeField(null=True, auto_now=False, auto_now_add=False)
    category = models.CharField(
        choices=CATEGORY_CHOICES, 
        max_length=50,
        default= TASK
    )
    possible_points = models.IntegerField()
    students_grades = models.ManyToManyField(CustomUser, related_name="grades")

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
        default=A,
        )
    point_grade = models.IntegerField()

class Attendance(models.Model):
    attendance_date = models.DateField(auto_now=False, auto_now_add=True)
    note = models.TextField(null = True, max_length=500)
    instructor = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    student = models.OneToOneField(CustomUser, null=True, related_name="student", on_delete=models.CASCADE)



class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    title = models.CharField( max_length=200)
    date_posted = models.DateTimeField( auto_now=False, auto_now_add=True)
    content = models.TextField(max_length=5000)
    docfile = models.FileField(upload_to='documents')
    # replies = models.ManyToManyField(CustomUser)

    def __str__(self):
        return f"{self.user.username} {self.course.name} {self.title}"
    