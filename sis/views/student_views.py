from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse

from ..forms import AddCourseForm, AddStaffForm, AddStudentForm, AddStudentToCourseForm, AssignmentForm, AttendanceReportForm, PostForm, AssignmentForm, AssignmentSubmissionForm,  AddMultipleChoiceQuestionForm, AddTestForm
from users.models import Course, CustomUser, Post, Grade, Assignment, AssignmentSubmission, AssignmentSubmissionFile, Attendance, AttendanceReport, AssignmentFile
from django.contrib import messages
from django.utils import timezone
from django.forms import modelformset_factory

def view_student_courses(request):
    student = CustomUser.objects.get(id=request.user.id)
    courses = student.course_set.all()

    print(courses)

    context = {
        "user":student,
        "courses": courses,
    }

    return render(request, "sis/student_templates/my_courses.html", context)


def grades(request):
    student = CustomUser.objects.get(id=request.user.id)
    courses = student.course_set.all()
    assigns = []
    for course in courses:
        assigns = [
            *assigns, 
            Assignment.objects.filter(
                course=course,
            )
        ]
    assigns = [*assigns]
    context  = {
        "user": student,
        "courses": courses,
        "assignments": assigns
    }

    return render(request, "sis/student_templates/grades.html", context)

