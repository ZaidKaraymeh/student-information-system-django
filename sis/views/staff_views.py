from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse

from ..forms import AddCourseForm, AddStaffForm, AddStudentForm, AddStudentToCourseForm, AssignmentForm, AttendanceReportForm, PostForm, AssignmentForm, AssignmentSubmissionForm,  AddMultipleChoiceQuestionForm, AddTestForm
from users.models import Course, CustomUser, Post, Grade, Assignment, AssignmentSubmission, AssignmentSubmissionFile, Attendance, AttendanceReport, AssignmentFile
from django.contrib import messages
from django.utils import timezone
from django.forms import modelformset_factory


def gradebook(request):
    instructor = CustomUser.objects.get(id=request.user.id)
    courses = Course.objects.filter(instructor=instructor)

    context = {
        "user":instructor,
        "courses": courses,
    }
    return render(request, "sis/admin_templates/gradebook.html", context)
def gradebook_course(request, course_id):
    course = Course.objects.get(id=course_id)
    instructor = CustomUser.objects.get(id=request.user.id)

    students = course.students.all()    

    print(students)


    context = {
        "user":instructor,
        "course": course,
        "students":students
    }
    return render(request, "sis/admin_templates/gradebook_course.html", context)

