from django.shortcuts import redirect, render
from ..forms import AddCourseForm, AddStudentForm
from users.models import Course, CustomUser
from django.contrib import messages


def add_course(request):
    if request.method == "POST":
        form = AddCourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"{form.cleaned_data.get('name')} has been added successfully!")
            return redirect("view_courses")
    else:
        form = AddCourseForm()
        form.fields["instructor"].queryset = CustomUser.objects.filter(user_type = "STA")    
    context = {"form":form}
    return render(request, "sis/admin_templates/add_course.html", context)

def manage_course(request):
    pass

def view_courses(request):
    courses = Course.objects.all()
    context = {"courses": courses}
    return render(request, "sis/admin_templates/view_courses.html", context)
def edit_course(request, id):
    course = Course.objects.get(id=id)
    if request.method == "POST":
        form = AddCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"{form.cleaned_data.get('code')} Section {form.cleaned_data.get('section')} has been Edited successfully!")
            return redirect("view_courses")
    else:
        form = AddCourseForm(instance=course)
        form.fields["instructor"].queryset = CustomUser.objects.filter(user_type = "STA")    
    context = {"form":form, "course":course}
    return render(request, "sis/admin_templates/edit_course.html", context)

def delete_course(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    messages.warning(request, f"{course.code} Section {course.section} has been deleted successfully!")
    return redirect("view_courses")




# STUDENT VIEWS

def add_student(request):
    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            f = form.save(commit = False)
            f.user_type = "STU"
            f.save()
            messages.success(request, f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')} has been added successfully!")
            return redirect("view_courses")
    else:
        form = AddStudentForm()
          
    context = {"form":form}
    return render(request, "sis/admin_templates/add_student.html", context)

def view_students(request):
    students = CustomUser.objects.filter(user_type = "STU")
    context = {"students": students}
    return render(request, "sis/admin_templates/view_students.html", context)

def view_student_enrolled_courses(request, id):
    courses_enrolled = Course.objects.filter(students__id = id)
    student = CustomUser.objects.get(id=id)
    context = {"courses": courses_enrolled, "student":student}
    print(courses_enrolled)
    return render(request, "sis/admin_templates/view_student_enrolled_courses.html", context)

