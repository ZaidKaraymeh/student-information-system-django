from django.shortcuts import redirect, render
from ..forms import AddCourseForm
from users.models import Course, CustomUser
from django.contrib import messages


def add_course(request):
    if request.method == "POST":
        form = AddCourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"{form.cleaned_data.get('name')} has been added successfully!")
            return redirect("home")
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
    context = {"form":form}
    return render(request, "sis/admin_templates/edit_course.html", context)
