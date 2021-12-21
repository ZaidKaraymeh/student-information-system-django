from django.shortcuts import redirect, render, HttpResponse

from ..forms import AddCourseForm, AddStaffForm, AddStudentForm, AddStudentToCourseForm, PostForm
from users.models import Course, CustomUser, Post, Assignment
from django.contrib import messages

import xlwt

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

def delete_course_enrolled(request, id, course_id, *args, **kwargs):
    course = Course.objects.get(id=course_id)
    user = CustomUser.objects.get(id=id)
    course.students.remove(user)
    messages.success(request, f"{course.code} Sec {course.section} has been dropped successfully from {user.first_name} {user.last_name} ")
    return redirect("view_student_enrolled_courses", id=id)

def view_courses(request):
    courses = Course.objects.all().order_by('code')
    context = {"courses": courses}
    return render(request, "sis/admin_templates/view_courses.html", context)

def export_courses(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="courses.xls"'   
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Courses Data') # this will make a sheet named Users Data
    
    # Sheet header, first row   
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Code', 'Course Name', 'Section', 'Instructor', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Course.objects.all().values_list('code', 'name', 'section', 'instructor')
    for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

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



def course_dashboard(request, id, instructor_id):
    course = Course.objects.get(id=id)
    if request.method == "POST":
        print(request.FILES)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            print("form is valid")
            f = form.save(commit= False)
            f.course = course
            print("form course",  f.course)
            f.user = CustomUser.objects.get(id=instructor_id)
            print("form user",  f.user)
            f.save()
            messages.success(
                request,
                f"Post Successful!"
            )
            return redirect("course_dashboard", id=id, instructor_id=instructor_id)
    else:
        form = PostForm()
    user = CustomUser.objects.get(id=instructor_id)
    print("user ", user)
    posts = Post.objects.filter(course__id = id)
    assignments = Assignment.objects.filter(course__id = id)
    print(posts)
    context = {
        'form':form, 
        "posts":posts, 
        "course": course, 
        "assignments":assignments
    }
    return render(request, "sis/admin_templates/course_dashboard.html", context)



# STUDENT VIEWS

def add_student(request):
    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            f = form.save(commit = False)
            f.user_type = "STU"
            f.username = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
            f.save()
            messages.success(request, f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')} has been added successfully!")
            return redirect("view_students")
    else:
        form = AddStudentForm()
          
    context = {"form":form}
    return render(request, "sis/admin_templates/add_student.html", context)

def view_students(request):
    students = CustomUser.objects.filter(user_type = "STU")
    context = {"students": students}
    return render(request, "sis/admin_templates/view_students.html", context)

def export_students(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="students.xls"'   
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Student Data') # this will make a sheet named Users Data
    
    # Sheet header, first row   
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['ID', 'First Name', 'Second Name', "Year", 'Email', 'Address', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = CustomUser.objects.filter(user_type="STU").values_list('id', 'first_name', 'last_name', 'year', 'email', 'address', )
    for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def view_student_enrolled_courses(request, id):
    courses_enrolled = Course.objects.filter(students__id = id)
    student = CustomUser.objects.get(id=id)
    if request.method == "POST":
        form = AddStudentToCourseForm(request.POST)
        if form.is_valid():
            f = form
            course_form = f.cleaned_data["courses"]
            course = Course.objects.get(id = course_form)
            user = CustomUser.objects.get(id=id)
            course.students.add(user)
            course.save()
            messages.success(request, f" {user.first_name} {user.last_name} has sucessfully enrolled in {course.code} Sec {course.section}!")
            return redirect("view_student_enrolled_courses", id=id)
    else:
        form = AddStudentToCourseForm()

          
    context = {"courses": courses_enrolled, "student":student, "form":form}
    return render(request, "sis/admin_templates/view_student_enrolled_courses.html", context)





def add_staff(request):
    if request.method == "POST":
        form = AddStaffForm(request.POST)
        if form.is_valid():
            f = form.save(commit = False)
            f.username = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
            f.user_type = "STA"
            f.save()
            messages.success(request, f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')} has been added successfully!")
            return redirect("view_staff")
    else:
        form = AddStaffForm()
          
    context = {"form":form}
    return render(request, "sis/admin_templates/add_staff.html", context)


def view_staff(request):
    staffs = CustomUser.objects.filter(user_type = "STA")
    context = {"staffs": staffs}
    return render(request, "sis/admin_templates/view_staff.html", context)

def view_instructor_enrolled_courses(request, id):
    courses_enrolled = Course.objects.filter(instructor__id = id)
    instructor = CustomUser.objects.get(id=id)

        
    context = {"courses": courses_enrolled, "instructor":instructor}
    return render(request, "sis/admin_templates/view_instructor_enrolled_courses.html", context)

# def edit_instructor_enrolled_courses(request, course_id, )

def export_staff(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="staff.xls"'   
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Staff Data') # this will make a sheet named Users Data
    
    # Sheet header, first row   
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['ID', 'First Name', 'Second Name', 'Email', 'Address', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = CustomUser.objects.filter(user_type="STA").values_list('id', 'first_name', 'last_name', 'email', 'address', )
    for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_staff_enrolled_course(request, id):
    instructor = CustomUser.objects.get(id=id)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f"attachment; filename={instructor.username}'s_enrolled_courses.xls"   
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Courses Teaching Data') # this will make a sheet named Users Data
    
    # Sheet header, first row   
    row_num = 1

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    ws.write(0, 0, f"{instructor.username}'s Classes")
    columns = ['Code', 'Course Name', 'Section', 'Instructor', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # courses_enrolled = Course.objects.filter(instructor__id = id)
    rows = Course.objects.filter(instructor__id=id).values_list('code', 'name', 'section', 'instructor')
    for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
def export_student_enrolled_course(request, id):
    student = CustomUser.objects.get(id=id)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f"attachment; filename={student.username}'s_enrolled_courses.xls"   
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Courses Teaching Data') # this will make a sheet named Users Data
    
    # Sheet header, first row   
    row_num = 1

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    ws.write(0, 0, f"{student.username}'s Classes")
    columns = ['Code', 'Course Name', 'Section' ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # courses_enrolled = Course.objects.filter(student__id = id)
    rows = Course.objects.filter(students__id=id).values_list('code', 'name', 'section')
    for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response



