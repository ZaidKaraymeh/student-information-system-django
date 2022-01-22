from django.shortcuts import redirect, render, HttpResponse

from ..forms import AddCourseForm, AddStaffForm, AddStudentForm, AddStudentToCourseForm, AssignmentForm, AttendanceReportForm, PostForm, AssignmentForm, AssignmentSubmissionForm,  AddMultipleChoiceQuestionForm, AddTestForm
from users.models import Course, CustomUser, Post, Grade, Assignment, AssignmentSubmission, AssignmentSubmissionFile, Attendance, AttendanceReport, AssignmentFile
from django.contrib import messages
from django.utils import timezone
from django.forms import modelformset_factory
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
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        form2 = AssignmentForm(request.POST, request.FILES)
        student_submission_form = AssignmentSubmissionForm(request.POST, request.FILES)
        if student_submission_form.is_valid():
            f = student_submission_form.save(commit=False)
            f.student = CustomUser.objects.get(id=request.user.id)
            f.instructor = CustomUser.objects.get(id=instructor_id)
            f.submitted_at = timezone.now()
            f.submitted = True
            grade = Grade.objects.create(
                course=course,
                student = CustomUser.objects.get(id=request.user.id)
            )
            grade.save()
            f.grade = grade
            f.save()
            for file in request.FILES.getlist('file'):
                obj = AssignmentSubmissionFile.objects.create(
                    file=file,
                    student = CustomUser.objects.get(id=request.user.id),
                )
                obj.save()
                f.files.add(obj)
                f.save()

            assignment = Assignment.objects.get(id=request.POST.get('assignment_id'))
            assignment.student_submissions.add(f)
            assignment.save()
            messages.success(request, "Assignment submitted successfully!")
            return redirect("course_dashboard", id=course.id, instructor_id=instructor_id)

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
            print("form course",  f.course)
            f.user = CustomUser.objects.get(id=instructor_id)
            print("form user",  f.user)
            f.save()
            messages.success(
                request,
                f"Post Successful!"
            )
            return redirect("course_dashboard", id=id, instructor_id=instructor_id)

        # student_assignment_submission_form = 
    else:
        form = PostForm()
        form2 = AssignmentForm()
        student_submission_form = AssignmentSubmissionForm()
        
    student_submission_form = AssignmentSubmissionForm()
    instructor = CustomUser.objects.get(id=instructor_id)
    user = CustomUser.objects.get(id=request.user.id)
    posts = Post.objects.filter(course__id = id).order_by("-date_posted")
    assignments = Assignment.objects.filter(course__id = id).order_by("-date_posted")
    students = CustomUser.objects.filter(course__id = id)
    context = {
        'form':form, 
        'form2':form2, 
        "posts":posts, 
        "course": course, 
        "assignments":assignments,
        "instructor":instructor,
        "user":user,
        "students":students,
        "student_submission_form":student_submission_form,
    }
    return render(request, "sis/admin_templates/course_dashboard.html", context)


def course_assignment_builder(request):
    assignments = Assignment.objects.all().order_by('-date_posted')
    print("plinker", assignments)
    if request.method == "POST":
        add_test_form = AddTestForm(request.POST or None)
        if add_test_form.is_valid():
            f = add_test_form.save(commit=False)
            f.save()
    else:
        add_test_form = AddTestForm()

    context = {
        'form':add_test_form,
        'assignments': assignments,
    }

    return render(request, 'sis/admin_templates/course_assignment_builder.html', context)

def course_assignment_build(request):
    user = CustomUser.objects.get(id=request.user.id)
    if request.method == "POST":
        add_assignment_form = AssignmentForm(request.POST or None, request.FILES)
        # file_form = AssignmentFileForm(request.POST, request.FILES)
        
        if add_assignment_form.is_valid():
            f = add_assignment_form.save(commit=False)
            course = Course.objects.get(id=add_assignment_form.cleaned_data['courses'])
            f.instructor = course.instructor
            f.course = course
            f.save()
            for file in request.FILES.getlist('file'):
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
                )
                grade.save()
                f.students_grades.add(grade)
                f.save()

            return redirect('course_assignment_builder')
    else:
        add_assignment_form = AssignmentForm()
        add_assignment_form.fields["courses"].queryset = Course.objects.filter(instructor__id = user.id)

    context = {
        'form':add_assignment_form,
    }
    return render(request, 'sis/admin_templates/add_assignment.html', context)

def course_assignment_edit(request, assignment_id):
    user = CustomUser.objects.get(id=request.user.id)
    instance = Assignment.objects.get(id=assignment_id)
    if request.method == "POST":
        assignment_form = AssignmentForm(request.POST or None, request.FILES, instance=instance)
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
        assignment_form = AssignmentForm(instance = instance)
        assignment_form.fields["courses"].queryset = Course.objects.filter(instructor__id = user.id)
    files = instance.files.all()
    context = {
        'form':assignment_form,
        'files':files,
    }
    return render(request, 'sis/admin_templates/edit_assignment.html', context)

def course_student_submission(request, course_id, assignment_id):
    print("reacing submission")
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
            grade, created = Grade.objects.get_or_create(
                course=course,
                student = CustomUser.objects.get(id=request.user.id)
            )
            grade.save()
            f.grade = grade
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

def view_attendance(request):
    courses = Course.objects.all()
    context = {"courses": courses}
    print("view attendance")
    # attendance = Attendance.objects.all()
    # context = {"attendance": attendance}
    return render(request, "sis/admin_templates/view_attendance.html", context)

def view_attendance_course(request, course_id):
    print("view_attendance_course")

    attendance = Attendance.objects.filter(course__id = course_id)
    course = Course.objects.get(id=course_id)
    context = {"attendance": attendance, "course": course}
    return render(request, "sis/admin_templates/view_attendance_course.html", context)

def view_attendance_course_report(request, attendance_id, course_id):
    attendance = AttendanceReport.objects.filter(attendance__id = attendance_id)
    print(attendance)
    course = Course.objects.get(id=course_id)
    date = attendance.first().attendance_date
    context = {
        "attendance": attendance,
        "course": course,
        'attendance_id':attendance_id,
        "date":date
    
    }
    # attendance = Attendance.objects.all()
    # context = {"attendance": attendance}
    return render(request, "sis/admin_templates/view_attendance_course_report.html", context)

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

def edit_attendance_course_report(request, course_id, attendance_id):
    attendance = AttendanceReport.objects.filter(attendance__id = attendance_id)
    attendance_reports = AttendanceReport.objects.filter(attendance__id = attendance_id)

    AttendenceReportFormSet = modelformset_factory(
        AttendanceReport, 
        form=AttendanceReportForm,
        extra=0,
        )

    if request.method == "POST":
        print("post")
        formset = AttendenceReportFormSet(
            request.POST, 
            queryset = attendance_reports
            )
        if formset.is_valid():
            formset.save()
            print("form is valid")
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
    }
    return render(request, 'sis/admin_templates/edit_attendance_course_report.html', context)