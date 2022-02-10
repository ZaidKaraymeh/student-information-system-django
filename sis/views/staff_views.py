from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse

from ..forms import AddCourseForm, AddStaffForm, AddStudentForm, AddStudentToCourseForm, AssignmentForm, AttendanceReportForm, PostForm, AssignmentForm, AssignmentSubmissionForm,  AddMultipleChoiceQuestionForm, AddTestForm, GradeForm
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


def gradebook_report(request, course_id, student_id):
    instructor = CustomUser.objects.get(id=request.user.id)
    course = Course.objects.get(id=course_id)
    student = CustomUser.objects.get(id=student_id)

    assigns = Assignment.objects.filter(course=course)

    context = {
        "user":instructor,
        "course": course,
        "student":student,
        "assignments": assigns,
    }
    return render(request, "sis/admin_templates/gradebook_report.html", context)

def gradebook_report_edit(request, course_id, student_id):
    instructor = CustomUser.objects.get(id=request.user.id)
    course = Course.objects.get(id=course_id)
    student = CustomUser.objects.get(id=student_id)

    assigns = Assignment.objects.filter(course=course)


    grades = Grade.objects.filter(student=student, course=course)


    GradeReportFormSet = modelformset_factory(
        Grade, 
        form=GradeForm,
        extra=0,
        )

    if request.method == "POST":
        print("post")
        formset = GradeReportFormSet(
            request.POST, 
            queryset = grades
            )
        if formset.is_valid():
            formset.save()
            print("form is valid")
            messages.success(request, "Grades updated successfully!")
            return redirect("gradebook_report", course_id=course_id, student_id=student_id )
    else:
        formset = GradeReportFormSet(queryset = grades)




    context = {
        "user":instructor,
        "course": course,
        "student":student,
        "assignments": assigns,
        "formset":formset,
    }
    return render(request, "sis/admin_templates/gradebook_report_edit.html", context)
