from http.client import HTTPResponse
from multiprocessing import context
from django.shortcuts import redirect, render, HttpResponse

from ..forms import AddCourseForm, AddFeeForm, AddFeeReportForm, AddStaffForm, AddStudentForm, AddStudentToCourseForm, AssignmentForm, AttendanceReportForm, PostForm, AssignmentForm, AssignmentSubmissionForm,  AddMultipleChoiceQuestionForm, AddTestForm, GradeWeightForm, SemesterForm
from users.models import Course, CustomUser, Post, Grade, Assignment, AssignmentSubmission, AssignmentSubmissionFile, Attendance, AttendanceReport, AssignmentFile, Fee, FeeReport, Semester
from django.contrib import messages
from django.utils import timezone
from django.forms import modelformset_factory
import xlwt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..decorators import is_admin, is_staff




@is_staff
def view_semesters_courses(request):
    user = CustomUser.objects.get(id=request.user.id)
    semesters = Semester.objects.all().order_by('-date_created')


    context = {
        'user':user,
        'semesters':semesters
    }

    return render(request, "sis/admin_templates/view_semesters_courses.html", context)
@is_admin
def add_semester(request):
    user = CustomUser.objects.get(id=request.user.id)
    last_semester_students = Semester.objects.last() if Semester.objects.last() != type(None) else None
    if request.method == "POST":
        form = SemesterForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            semesters = Semester.objects.all().order_by('-date_created')
            if not f.archive:
                for semester in semesters:
                    semester.archive = True
                    semester.save()
            
            f.save()
            if last_semester_students != None:
                for student in last_semester_students.students.all():
                    f.students.add(student)
                f.save()

            fee = Fee.objects.create(
                fee_year = f.year,
                amount_needed=500,
                note = "---",
            )
            fee.save()
            f.fees.add(fee)
            f.save()
            if last_semester_students != None:
                for student in last_semester_students.students.all():
                    report, created = FeeReport.objects.get_or_create(
                    student = student,
                    defaults={
                        'note': "---",
                        "amount_paid": 0,
                        "paid_full":False,
                        },
                    )
                    fee.student_fees.add(report)
                    fee.save()
            
            messages.success(request, f"Semester Added Successfully!")
            return redirect("dashboard")
    else:
        form = SemesterForm()


    context = {
        'user':user,
        'form': form,
    }
    return render(request, "sis/admin_templates/add_semester.html", context)
@is_admin
def edit_semester(request, semester_id):
    user = CustomUser.objects.get(id=request.user.id)
    semester = Semester.objects.get(id=semester_id)
    if request.method == "POST":
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            form.save()
            messages.success(request, f"Semester Editted Successfully!")
            return redirect("view_semesters")
    else:
        form = SemesterForm(instance=semester)


    context = {
        'user':user,
        'form': form,
    }
    return render(request, "sis/admin_templates/edit_semester.html", context)

@is_admin
def add_course(request, semester_id):
    user = CustomUser.objects.get(id=request.user.id)
    semester = Semester.objects.get(id=semester_id)
    if request.method == "POST":
        form = AddCourseForm(request.POST)
        weight_form = GradeWeightForm(request.POST)
        if form.is_valid() and weight_form.is_valid():
            w = weight_form.save()

            f = form.save(commit=False)
            f.weight = w
            f.year = semester.year
            f.save()
            w.save()
            semester.courses.add(f)
            semester.save()
            messages.success(request, f"{form.cleaned_data.get('name')} has been added successfully!")
            return redirect("view_courses", semester_id=semester_id)
    else:
        form = AddCourseForm()
        weight_form = GradeWeightForm()
        form.fields["instructor"].queryset = semester.staff.all()    
    context = {
        "form":form,
        "user":user,
        "weight_form":weight_form,
        'semester':semester,
        }
    return render(request, "sis/admin_templates/add_course.html", context)

def manage_course(request):
    pass
@is_admin
def delete_course_enrolled(request, id, course_id, *args, **kwargs):
    course = Course.objects.get(id=course_id)
    user = CustomUser.objects.get(id=id)
    course.students.remove(user)
    messages.success(request, f"{course.code} Sec {course.section} has been dropped successfully from {user.first_name} {user.last_name} ")
    return redirect("view_student_enrolled_courses", id=id)

def view_courses(request, semester_id):
    user = CustomUser.objects.get(id=request.user.id)
    semester = Semester.objects.get(id=semester_id)

    if user.user_type == "STA":
        courses = semester.courses.filter(instructor__id = user.id).order_by('code')
    else:
        courses = Course.objects.filter(semester__id=semester_id).order_by('code')
    context = {
        "courses": courses,
        "user":user,
        'semester':semester,
        }
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

@is_admin
def edit_course(request, id, semester_id):
    course = Course.objects.get(id=id)
    weight = course.weight
    user = CustomUser.objects.get(id=request.user.id)
    semester = Semester.objects.get(id=semester_id)
    if request.method == "POST":
        form = AddCourseForm(request.POST, instance=course)
        weight_form = GradeWeightForm(request.POST, instance=weight)
        if form.is_valid() and weight_form.is_valid():
            weight_form.save()
            form.save()
            messages.success(request, f"{form.cleaned_data.get('code')} Section {form.cleaned_data.get('section')} has been Edited successfully!")
            return redirect("view_courses", semester_id=semester_id)
    else:
        form = AddCourseForm(instance=course)
        weight_form = GradeWeightForm(instance=weight)
        form.fields["instructor"].queryset = semester.staff.all()
    context = {
        "form":form, 
        "course":course,
        "user":user,
        "weight_form": weight_form,
        'semester':semester,
        }
    return render(request, "sis/admin_templates/add_course.html", context)

@is_admin
def delete_course(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    messages.warning(request, f"{course.code} Section {course.section} has been deleted successfully!")
    return redirect("view_courses")






# STUDENT VIEWS

def add_student(request, semester_id):
    user = CustomUser.objects.get(id=request.user.id)
    semester = Semester.objects.get(id=semester_id)

    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            f = form.save(commit = False)
            f.user_type = "STU"
            f.username = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
            f.save()
            semester.students.add(f)
            fee = semester.fees.last()
            report, created = FeeReport.objects.get_or_create(
            student = f,
            defaults={
                'note': "---",
                "amount_paid": 0,
                "paid_full":False,
                },
            )
            if created:
                fee.student_fees.add(report)
            fee.save()

            messages.success(request, f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')} has been added successfully!")
            return redirect("view_students", semester_id=semester_id)
    else:
        form = AddStudentForm()
          
    context = {
        "form":form,
        "user":user,
        'semester':semester
        }
    return render(request, "sis/admin_templates/add_student.html", context)

def view_semesters_students(request):
    user = CustomUser.objects.get(id=request.user.id)
    semesters = Semester.objects.all().order_by('-date_created')
    context = {
        "semesters": semesters,
        "user":user
        }
    return render(request, "sis/admin_templates/view_semesters_students.html", context)

def view_semesters_staff(request):
    user = CustomUser.objects.get(id=request.user.id)
    semesters = Semester.objects.all().order_by('-date_created')
    context = {
        "semesters": semesters,
        "user":user
        }
    return render(request, "sis/admin_templates/view_semesters_staff.html", context)

def view_students(request, semester_id):
    user = CustomUser.objects.get(id=request.user.id)
    students = CustomUser.objects.filter(user_type = "STU", semester__id=semester_id)
    semester = Semester.objects.get(id=semester_id)

    context = {
        "students": students,
        "user":user,
        'semester':semester
        }
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

def get_student_courses(semester_id):
            COURSE_CHOICES = [
                (
                    course.id ,
                    f"{course.code} {course.name} Sec {course.section} {course.year}"
                    ) for course in Course.objects.filter(semester__id=semester_id).order_by('code')
            ]
            return COURSE_CHOICES

def view_student_enrolled_courses(request, id, semester_id):

    user = CustomUser.objects.get(id=request.user.id)
    choices = get_student_courses(semester_id)
    courses_enrolled = Course.objects.filter(students__id = id)
    student = CustomUser.objects.get(id=id)
    user = CustomUser.objects.get(id=request.user.id)
    semester = Semester.objects.get(id=semester_id)
    assigns = []
    for course in courses_enrolled:
        assigns = [
            *assigns, 
            Assignment.objects.filter(
                course=course,
            )
        ]
    assigns = [*assigns]
    if request.method == "POST":
        form = AddStudentToCourseForm(choices, request.POST)
        if form.is_valid():
            f = form
            course_form = f.cleaned_data["courses"]
            course = Course.objects.get(id = course_form)
            user = CustomUser.objects.get(id=id)
            course.students.add(user)
            course.save()

            try:
                assignments = Assignment.objects.filter(course=course)
                for assignment in assignments:
                    grade = Grade.objects.create(
                        student=student,
                        course = course,
                        possible_points = assignment.possible_points,
                    )
                    grade.save()
                    assignment.students_grades.add(grade)
                    assignment.save()
            except:
                pass

            messages.success(request, f" {user.first_name} {user.last_name} has sucessfully enrolled in {course.code} Sec {course.section}!")
            return redirect("view_student_enrolled_courses", id=id, semester_id=semester_id)
            
    else:
    
        form = AddStudentToCourseForm(choices=get_student_courses(semester_id))


    
          
    context = {
        "courses": courses_enrolled, 
        "student":student, 
        "form":form,
        "user":user,
        "assignments":assigns,
        'semester':semester,
        }
    return render(request, "sis/admin_templates/view_student_enrolled_courses.html", context)

def view_student_enrolled_grades(request, student_id):
    student = CustomUser.objects.get(id=student_id)
    user = CustomUser.objects.get(id=request.user.id)
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

    # assigns_sorted = sorted(
    #     assigns,
    #     key= lambda x: (x["date_posted"], x[""])
    # )

    context  = {
        "user": user,
        "student": student,
        "courses": courses,
        "assignments": assigns
    }

    return render(request, "sis/admin_templates/view_student_enrolled_grades.html", context)



@is_admin
def add_staff(request, semester_id):
    user = CustomUser.objects.get(id=request.user.id)
    semester = Semester.objects.get(id=semester_id)
    if request.method == "POST":
        form = AddStaffForm(request.POST)
        if form.is_valid():
            f = form.save(commit = False)
            f.username = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}"
            f.user_type = "STA"
            f.save()
            semester.staff.add(f)
            semester.save()
            messages.success(request, f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')} has been added successfully!")
            return redirect("view_staff", semester_id=semester_id)
    else:
        form = AddStaffForm()
          
    context = {
        "form":form,
        "user":user,
        "semester":semester,
        }
    return render(request, "sis/admin_templates/add_staff.html", context)

@is_admin
def view_staff(request, semester_id):
    user = CustomUser.objects.get(id=request.user.id)
    semester = Semester.objects.get(id=semester_id)
    staffs = semester.staff.all()

    context = {
        "staffs": staffs,
        "user":user,
        "semester":semester,
        }
    return render(request, "sis/admin_templates/view_staff.html", context)


def view_instructor_enrolled_courses(request, id, semester_id):
    user = CustomUser.objects.get(id=request.user.id)
    courses_enrolled = Course.objects.filter(instructor__id = id)
    instructor = CustomUser.objects.get(id=id)
    semester = Semester.objects.get(id=semester_id)

        
    context = {
        "courses": courses_enrolled, 
        "instructor":instructor,
        "semester":semester,
        "user":user
        }
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


"""

def course_test_builder(request, course_id, instructor_id, quiz_type, *args, **kwargs):
    try:
        user = CustomUser.objects.filter(request.user.id)
        if user.user_type != "STA" or user.user_type != "ADM":
            return redirect('course_dashboard', id=course_id, instructor_id=instructor_id)

    except:
        return redirect('course_dashboard', id=course_id, instructor_id=instructor_id)
    course = Course.objects.filter(id=course_id)
    instructor = CustomUser.objects.filter(id=instructor_id)


    if request.method == "POST":
        add_test_form = AddTestForm(request.POST or None)
        if add_test_form.is_valid():
            f = add_test_form.save(commit=False)
            f.quiz_type = quiz_type
            f.course = course
            f.instructor = instructor
            f.save()
    else:
        add_test_form = AddTestForm()

    context = {
        'form':add_test_form,
        'course': course,
        'instructor': instructor
    }

    return render(request, 'sis/admin_templates/course_test_builder', context)

"""


def course_dashboard(request, id, instructor_id):
    course = Course.objects.get(id=id)
    inst = CustomUser.objects.get(id=instructor_id)
    choices = [
        (
            course.id ,
            f"{course.code} {course.name} Sec {course.section}"
            ) for course in Course.objects.filter(instructor__id=inst.id).order_by('code')
    ]
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        form2 = AssignmentForm(request.POST, request.FILES)
        student_submission_form = AssignmentSubmissionForm(request.POST, request.FILES)
        
        if form2.is_valid():
            f = form2.save(commit= False)
            f.course = course
            f.instructor = CustomUser.objects.get(id=instructor_id)
            f.save()
            messages.success(
                request,
                f"Assignment Posted Successful!"
            )
            return redirect("course_dashboard", id=id, instructor_id=instructor_id)

        if form.is_valid():
            f = form.save(commit= False)
            f.course = course
            user = CustomUser.objects.get(id =request.user.id)
            f.user = CustomUser.objects.get(id=user.id)
            f.save()
            messages.success(
                request,
                f"Post Successful!"
            )
            return redirect("course_dashboard", id=id, instructor_id=instructor_id)
        if student_submission_form.is_valid():
            desc = student_submission_form.cleaned_data['description']
            f = AssignmentSubmission.objects.create(
                student = CustomUser.objects.get(id=request.user.id),
                instructor = CustomUser.objects.get(id=instructor_id),
                submitted = True,
                course = course,
                description= desc,
            )

            # grade = Grade.objects.create(
            #     course=course,
            #     student = CustomUser.objects.get(id=request.user.id)
            # )
            # grade.save()
            # f.grade = grade
            f.save()
            for file in request.FILES.getlist('file'):
                print(file)
                obj = AssignmentSubmissionFile.objects.create(
                    files=file,
                    student = CustomUser.objects.get(id=request.user.id),
                )
                obj.save()
                f.files.add(obj)
                f.save()
            print(f.files.all())
            assignment = Assignment.objects.get(id=request.POST.get('assignment_id'))
            assignment.student_submissions.add(f)
            assignment.save()
            messages.success(request, "Assignment submitted successfully!")
            return redirect("course_dashboard", id=course.id, instructor_id=instructor_id)

        # student_assignment_submission_form = 
    else:
        form = PostForm()
        form2 = AssignmentForm()
        student_submission_form = AssignmentSubmissionForm()
        
    student_submission_form = AssignmentSubmissionForm()
    instructor = CustomUser.objects.get(id=instructor_id)
    user = CustomUser.objects.get(id=request.user.id)
    posts = Post.objects.filter(course__id = id).order_by("-date_posted")

    page = request.GET.get('page', 1)
    post_paginator = Paginator(posts, 10)
    try:
        posts_paginated = post_paginator.page(page)
    except PageNotAnInteger:
        posts_paginated = post_paginator.page(1)
    except EmptyPage:
        posts_paginated = post_paginator.page(post_paginator.num_pages)

    # if user.user_type == "STA":
    #     assignments = Assignment.objects.filter(course__id = id).order_by("-date_posted")
    # else:
    #     assignments = Assignment.objects.filter(course__id = id, ).order_by("-date_posted")

    assignments = Assignment.objects.filter(course__id = id).order_by("-date_posted")

    students = CustomUser.objects.filter(course__id = id)

    time_now = timezone.now()

    context = {
        'form':form, 
        'form2':form2, 
        "posts":posts_paginated, 
        "course": course, 
        "assignments":assignments,
        "instructor":instructor,
        "user":user,
        "students":students,
        "student_submission_form":student_submission_form,
        "time_now": time_now,
    }
    return render(request, "sis/admin_templates/course_dashboard.html", context)

@is_staff
def course_assignment_builder(request, course_id):

    user = CustomUser.objects.get(id = request.user.id)
    course = Course.objects.get(id=course_id)
    if user.user_type == "STA":
        assignments = course.assignments.all().order_by('-date_posted')
    else:
        assignments = Assignment.objects.all().order_by('-date_posted')

    semester = Semester.objects.filter(courses__id=course_id).first()
    context = {
        'assignments': assignments,
        "user":user,
        'course':course,
        'semester':semester
    }

    return render(request, 'sis/admin_templates/course_assignment_builder.html', context)

@is_staff
def course_assignment_build(request, course_id):
    user = CustomUser.objects.get(id=request.user.id)
    course = Course.objects.get(id=course_id)
    choices = [
        (
            course.id ,
            f"{course.code} {course.name} Sec {course.section}"
            ) for course in Course.objects.filter(instructor__id=user.id).order_by('code')
    ]
    if request.method == "POST":

        add_assignment_form = AssignmentForm(choices, request.POST or None, request.FILES)
        # file_form = AssignmentFileForm(request.POST, request.FILES)
        
        if add_assignment_form.is_valid():
            f = add_assignment_form.save(commit=False)
            f.instructor = course.instructor
            f.course = course
            f.save()
            files = request.FILES.getlist('file')
            print(files)
            for file in files:
                obj = AssignmentFile.objects.create(
                    file=file,
                    instructor = f.instructor,
                )
                obj.save()
                f.files.add(obj)
                f.save()
            students = f.course.students.all()
            for student in students:
                grade = Grade.objects.create(
                    student=student,
                    course = course,
                    possible_points = f.possible_points,
                )
                grade.save()
                f.students_grades.add(grade)
                f.save()
            course.assignments.add(f)
            course.save()
            messages.success(request, "Assignment Posted Successfully!")
            return redirect('course_assignment_builder', course.id)
    else:
        add_assignment_form = AssignmentForm(choices)
        # courses = Course.objects.filter(instructor__id = user.id)
        # add_assignment_form.fields["courses"].filter(lambda x:x in courses, courses)

    context = {
        'form':add_assignment_form,
        "user":user,
        'course':course,
    }
    return render(request, 'sis/admin_templates/add_assignment.html', context)

@is_staff
def view_assignment_submissions(request, assignment_id):
    user = CustomUser.objects.get(id=request.user.id)
    assignment = Assignment.objects.get(id=assignment_id)
    course = Course.objects.filter(assignments__id=assignment_id).first()

    context = {
        "user":user,
        'course':course,
        'assignment':assignment,

    }
    return render(request, 'sis/admin_templates/view_students_assignment_submissions.html', context)
@is_staff
def view_assignment_submissions_files(request, submission_report_id):
    user = CustomUser.objects.get(id=request.user.id)
    submission = AssignmentSubmission.objects.get(id=submission_report_id)
    print(submission_report_id)
    assignment = Assignment.objects.filter(student_submissions__id=submission_report_id).first()
    course = Course.objects.filter(assignments__id=assignment.id).first()
    print(submission.files.all())
    context = {
        "user":user,
        'course':course,
        'assignment':assignment,
        'submission':submission,

    }
    return render(request, 'sis/admin_templates/view_students_assignment_submissions_files.html', context)

@is_staff
def course_assignment_edit(request, assignment_id):
    user = CustomUser.objects.get(id=request.user.id)
    choices = [
        (
            course.id ,
            f"{course.code} {course.name} Sec {course.section}"
            ) for course in Course.objects.filter(instructor__id=user.id).order_by('code')
    ]
    instance = Assignment.objects.get(id=assignment_id)
    course = Course.objects.filter(assignments__id=assignment_id).first()
    print(course)
    if request.method == "POST":
        assignment_form = AssignmentForm(choices, request.POST or None, request.FILES, instance=instance)
        # file_form = AssignmentFileForm(request.POST, request.FILES)
        
        if assignment_form.is_valid():
            f = assignment_form.save(commit=False)
            f.save()
            for file in request.FILES.getlist('file'):
                obj = AssignmentFile.objects.create(
                    file=file,
                    instructor = f.instructor,
                )
                obj.save()
                f.files.add(obj)
                f.save()
            messages.success(request, "Assignment editted successfully!")
            return redirect('course_assignment_builder')
    else:
        assignment_form = AssignmentForm(choices, instance = instance)
    files = instance.files.all()
    context = {
        'form':assignment_form,
        'files':files,
        "user":user,
        'course': course,
        'assignment': instance,
    }
    return render(request, 'sis/admin_templates/edit_assignment.html', context)

def course_assignment_delete(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    course = Course.objects.filter(assignments__id=assignment_id).first()
    assignment.delete()
    messages.success(request, "Assignment Deleted successfully!")
    return redirect('course_assignment_builder', course_id=course.id)


def course_student_submission(request, course_id, assignment_id):
    course = Course.object.get(id=course_id)
    instructor = course.instructor
    if request.method == "POST":
        student_submission_form = AssignmentSubmissionForm(request.POST, request.FILES)
        if student_submission_form.is_valid():
            f = student_submission_form.save(commit=False)
            f.student = CustomUser.objects.get(id=request.user.id)
            f.instructor = CustomUser.objects.get(id=instructor.id)
            f.submitted_at = timezone.now()
            f.submitted = True
            f.save()
            for file in request.FILES.getlist('file'):
                obj = AssignmentSubmissionFile.objects.create(
                    file=file,
                    student = CustomUser.objects.get(id=request.user.id),
                )
                obj.save()
                f.files.add(obj)
                f.save()
            assignment = Assignment.objects.get(id=assignment_id)
            assignment.student_submissions.add(f)
            messages.success(request, "Assignment submitted successfully!")
            return redirect("course_dashboard", id=course.id, instructor_id=instructor.id)

    messages.add_message(request, 99, "Get request!", "danger")
    return redirect("course_dashboard", id=course.id, instructor_id=instructor.id)
# Attendance

@is_staff
def view_semesters_attendance(request):
    user = CustomUser.objects.get(id=request.user.id)
    semesters = Semester.objects.all().order_by('-date_created')

    context = {
        'user':user,
        'semesters':semesters
    }

    return render(request, "sis/admin_templates/view_semesters_attendance.html", context)
@is_staff
def view_attendance(request, semester_id):
    user = CustomUser.objects.get(id = request.user.id)
    semester = Semester.objects.get(id=semester_id)
    if user.user_type == "STA":
        courses = semester.courses.filter(instructor__id=user.id)
    else:
        courses = semester.courses.all()
    context = {
        "courses": courses,
        "user":user,
        "semester":semester
    }
    # attendance = Attendance.objects.all()
    # context = {"attendance": attendance}
    return render(request, "sis/admin_templates/view_attendance.html", context)

@is_staff
def view_attendance_course(request, course_id):
    user = CustomUser.objects.get(id=request.user.id)

    attendance = Attendance.objects.filter(course__id = course_id)
    course = Course.objects.get(id=course_id)
    semester = Semester.objects.filter(courses__id=course_id).first()
    context = {
        "attendance": attendance, 
        "course": course,
        "user":user,
        "semester":semester,
        
    }
    return render(request, "sis/admin_templates/view_attendance_course.html", context)

@is_staff
def view_attendance_course_report(request, attendance_id, course_id):
    user = CustomUser.objects.get(id=request.user.id)
    attendance = AttendanceReport.objects.filter(attendance__id = attendance_id)
    course = Course.objects.get(id=course_id)
    date = attendance.first().attendance_date
    context = {
        "attendance": attendance,
        "course": course,
        'attendance_id':attendance_id,
        "date":date,
        "user":user
    
    }
    # attendance = Attendance.objects.all()
    # context = {"attendance": attendance}
    return render(request, "sis/admin_templates/view_attendance_course_report.html", context)

@is_staff
def add_attendance_course_report(request, course_id):
    course = Course.objects.get(id=course_id)
    instructor = course.instructor
    obj, created = Attendance.objects.get_or_create(
            date_now = timezone.now().date(),
            course=course, 
            instructor = course.instructor
    )

    if created:
        students = course.students.all()
        for student in students:
            report = AttendanceReport.objects.create(
                attendance_date = timezone.now().date(), 
                instructor = instructor, 
                course=course, 
                is_absent=False, 
                student=student 
            )
            obj.attendance_reports.add(report)
            obj.save()
        messages.success(request, "Today's attendance has been added successfully!")
        return redirect("view_attendance_course_report", attendance_id=obj.id, course_id=course_id )
    else:
        messages.add_message(request, 99,  "Today's attendance has already been created", "danger")
        return redirect("view_attendance_course", course_id=course_id)

@is_staff
def edit_attendance_course_report(request, course_id, attendance_id):
    user = CustomUser.objects.get(id=request.user.id)

    attendance = AttendanceReport.objects.filter(attendance__id = attendance_id)
    attendance_reports = AttendanceReport.objects.filter(attendance__id = attendance_id)

    AttendenceReportFormSet = modelformset_factory(
        AttendanceReport, 
        form=AttendanceReportForm,
        extra=0,
        )

    if request.method == "POST":
        formset = AttendenceReportFormSet(
            request.POST, 
            queryset = attendance_reports
            )
        if formset.is_valid():
            formset.save()
            messages.success(request, "Attendance updated successfully!")
            return redirect("view_attendance_course_report", attendance_id=attendance_id, course_id=course_id )
    else:
        formset = AttendenceReportFormSet(queryset = attendance_reports)

    course = Course.objects.get(id=course_id)

    context = {
        'formset':formset,
        'course':course,
        'attendance':attendance,
        'attendance_id':attendance_id,
        "user":user
    }
    return render(request, 'sis/admin_templates/edit_attendance_course_report.html', context)

@is_admin
def dashboard(request):
    user = CustomUser.objects.get(id=request.user.id)
    semesters = Semester.objects.all().order_by('-date_created')
    # reports = AttendanceReport.objects.all()
    # attendance_present = 0

    # attendance_total = 0
    # attendance_absent = attendance_total - attendance_present
    # for report in reports:
    #     if report.is_absent == False:
    #         attendance_present += 1

    #     attendance_total += 1

    # attendance_present_percentage =   str(round(attendance_present/attendance_total, 4)*100)
    


    context = {
        # "attendance_total": attendance_total,
        # "attendance_present": attendance_present,
        # "attendance_absent": attendance_absent,
        # "attendance_present_percentage": attendance_present_percentage,
        "user":user,
        'semesters':semesters,

    }
    return render(request, "sis/admin_templates/view_semesters.html", context)

@is_admin
def fees(request, semester_id):
    user = CustomUser.objects.get(id=request.user.id)
    fees = Fee.objects.filter(semester__id=semester_id)
    semester = Semester.objects.get(id=semester_id)
    
    context = {
        "user": user,
        "fees": fees,
        'semester':semester
    }
    return render(request, "sis/admin_templates/fees.html", context)

@is_admin
def add_fee(request, semester_id):
    user = CustomUser.objects.get(id=request.user.id)
    semester = Semester.objects.get(id=semester_id)
    if request.method == "POST":
        form = AddFeeForm(request.POST)
        if form.is_valid():
            f= form.save(commit=False)
            f.fee_year = semester.year
            f.save()
            semester.fees.add(f)
            semester.save()
            messages.success(request, "Fee Added successfully!")
            return redirect("fees", semester_id=semester_id)
    else:
        form = AddFeeForm()

    context = {
        "form": form,
        "user": user,
        'semester':semester,
    }

    return render(request, "sis/admin_templates/add_fee.html", context)

@is_admin
def edit_fee(request, fee_id, semester_id):
    user = CustomUser.objects.get(id=request.user.id)
    semester = Semester.objects.get(id=semester_id)
    fee = Fee.objects.get(id=fee_id)
    if request.method == "POST":
        form = AddFeeForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            messages.success(request, "Fee Added successfully!")
            return redirect("fees")
    else:
        form = AddFeeForm(instance=fee)

    context = {
        "form": form,
        "user": user,
        "semester":semester,
    }

    return render(request, "sis/admin_templates/add_fee.html", context)

@is_admin
def edit_fee_report(request, report_id):
    user = CustomUser.objects.get(id=request.user.id)
    obj = FeeReport.objects.get(id=report_id)
    fee = Fee.objects.get(student_fees__id=report_id)
    student = obj.student
    if request.method == "POST":
        form = AddFeeReportForm(request.POST, instance=obj)
        if form.is_valid():
            inst = form.save(commit=False)
            if fee.amount_needed <= inst.amount_paid:
                inst.paid_full = True
            else:
                inst.paid_full = False
            inst.save()
            messages.success(request, "Fee Edited successfully!")
            return redirect("fee_instance", fee_id=fee.id)
    else:
        form = AddFeeReportForm(instance=obj)

    context = {
        "form": form,
        "user": user,
        "student": student,
    }

    return render(request, "sis/admin_templates/edit_fee_report.html", context)


@is_admin
def fee_instance(request, fee_id, semester_id):
    user = CustomUser.objects.get(id=request.user.id)
    fee = Fee.objects.get(id=fee_id)
    semester = Semester.objects.get(id=semester_id)



    context = {
        "user": user,
        "fees": fee,
        'semester':semester,
    }
    return render(request, "sis/admin_templates/fee_instance.html", context)

    

def fees_student_portal(request, student_id, semester_id):
    semester = Semester.objects.get(id=semester_id)
    user = CustomUser.objects.get(id=request.user.id)
    student = CustomUser.objects.get(id=student_id)

    if student != user and user == "STU":
        return HTTPResponse("Acess Denied")

    fee = Fee.objects.filter(semester__id=semester_id)
    report, created = FeeReport.objects.get_or_create(
    student = student,
    defaults={
        'note': "---",
        "amount_paid": 0,
        "paid_full":False,
        },
    )
    
    if created:
        fee.student_fees.add(report)

    context = {
        "user":user,
        "student":student,
        "report":report,
        "fee":fee,
        'semester':semester,

    }
    return render(request, "sis/admin_templates/fee_report.html", context)
    

@is_admin
def view_semesters_fees(request):
    user = CustomUser.objects.get(id=request.user.id)
    semesters = Semester.objects.all().order_by('-date_created')


    context = {
        'user':user,
        'semesters':semesters
    }

    return render(request, "sis/admin_templates/view_semesters_fees.html", context)