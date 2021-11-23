from django.db import models
from django.contrib.auth.models import User

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


    address = models.TextField(null=True, max_length=500)
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

# class Student(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)

#     class Meta:
#         permissions = [("can_post_assignments", "Can post assignments")]

# class Instructor(Profile):
#     class Meta:
#         permissions = [("can_create_assignments", "Can create assignments")]