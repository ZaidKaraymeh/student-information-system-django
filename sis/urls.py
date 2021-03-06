from django.urls import path, include
from .views import views
from .views import admin_views
from .views import student_views
from .views import staff_views
urlpatterns = [
    path("", views.home, name="home" ),
    path("sis/", views.home_sis, name="home_sis" ),

    path("sis/add_course/<int:semester_id>", admin_views.add_course, name="add_course" ),

    path("sis/view_semesters_courses", admin_views.view_semesters_courses, name="view_semesters_courses"),
    path("sis/view_semesters_staff", admin_views.view_semesters_staff, name="view_semesters_staff"),
    path("sis/add_semester", admin_views.add_semester, name="add_semester"),
    path("sis/edit_semester/<int:semester_id>", admin_views.edit_semester, name="edit_semester"),
    path("sis/view_courses/semester/<int:semester_id>", admin_views.view_courses, name="view_courses"),
    path("sis/edit_course/<int:id>/<int:semester_id>", admin_views.edit_course, name="edit_course"),
    path("sis/delete_course/<int:id>", admin_views.delete_course, name="delete_course"),
    path("sis/export/courses", admin_views.export_courses, name="export_courses"),
    path("sis/course_dashboard/<int:id>/<int:instructor_id>", admin_views.course_dashboard, name="course_dashboard"),
    path("sis/courses/", student_views.view_student_courses, name="my_courses"),
    path("sis/fees/fees_report/<int:student_id>/<int:semester_id>", admin_views.fees_student_portal, name="fees_report"),
    path("sis/fees/fees_report/edit/<int:report_id>/", admin_views.edit_fee_report, name="edit_fee_report"),
    path("sis/fees/", admin_views.view_semesters_fees, name="view_semesters_fees"),
    path("sis/fees/semester/<int:semester_id>", admin_views.fees, name="fees"),
    path("sis/add_fee/<int:semester_id>", admin_views.add_fee, name="add_fee"),
    path("sis/edit_fee/<int:fee_id>/<int:semester_id>", admin_views.edit_fee, name="edit_fee"),
    path("sis/fee_instance/<int:fee_id>", admin_views.fee_instance, name="fee_instance"),
    path("sis/fee_instance/<int:fee_id>/<int:semester_id>", admin_views.fee_instance, name="fee_instance"),

    # STUDENT URLS
    path("sis/add_student/<int:semester_id>", admin_views.add_student, name="add_student" ),
    path("sis/view_students/<int:semester_id>", admin_views.view_students, name="view_students"),
    path("sis/view_semesters_students", admin_views.view_semesters_students, name="view_semesters_students"),
    path("sis/view_student_enrolled_courses/<int:id>/<int:semester_id>", admin_views.view_student_enrolled_courses, name="view_student_enrolled_courses"),
    path("sis/view_student_enrolled_grades/<int:student_id>/", admin_views.view_student_enrolled_grades, name="view_student_enrolled_grades"),
    path("sis/delete_student_enrolled/<slug:course_id>/<int:id>/", admin_views.delete_course_enrolled, name="delete_student_enrolled"),
    path("sis/export/students", admin_views.export_students, name="export_students"),
    path("sis/export/student/classes/<int:id>", admin_views.export_student_enrolled_course, name="export_student_enrolled_course"),
    path("sis/grades", student_views.grades, name="grades"),

    # STAFF URLS

    path("sis/add_staff/<int:semester_id>", admin_views.add_staff, name="add_staff" ),
    path("sis/course_assignment_builder/<int:course_id>", admin_views.course_assignment_builder, name="course_assignment_builder" ),
    path("sis/course_assignment_builder/view_assignment_submissions/<int:assignment_id>", admin_views.view_assignment_submissions, name="view_assignment_submissions" ),
    path("sis/course_assignment_builder/view_assignment_submissions/files/<int:submission_report_id>", admin_views.view_assignment_submissions_files, name="view_assignment_submissions_files" ),
    path("sis/course_assignment_builder/add_assignment/<int:course_id>", admin_views.course_assignment_build, name="course_assignment_build" ),
    path("sis/course_assignment_builder/edit_assignment/<int:assignment_id>", admin_views.course_assignment_edit, name="course_assignment_edit" ),
    path("sis/course_assignment_builder/delete_assignment/<int:assignment_id>", admin_views.course_assignment_delete, name="course_assignment_delete" ),
    path("sis/view_staff/<int:semester_id>", admin_views.view_staff, name="view_staff"),
    path("sis/view_instructor_enrolled_courses/<int:id>/<int:semester_id>", admin_views.view_instructor_enrolled_courses, name="view_instructor_enrolled_courses"),
    path("sis/view_attendance/", admin_views.view_semesters_attendance, name="view_semesters_attendance"),
    path("sis/view_attendance/semester/<int:semester_id>", admin_views.view_attendance, name="view_attendance"),
    path("sis/view_attendance/<int:course_id>/", admin_views.view_attendance_course, name="view_attendance_course"),
    path("sis/view_attendance_report/<int:attendance_id>/<int:course_id>/", admin_views.view_attendance_course_report, name="view_attendance_course_report"),
    path("sis/edit_attendance_report/<int:attendance_id>/<int:course_id>/", admin_views.edit_attendance_course_report, name="edit_attendance_course_report"),
    path("sis/add_attendance_report/<int:course_id>/", admin_views.add_attendance_course_report, name="add_attendance_course_report"),
    path("sis/export/staff", admin_views.export_staff, name="export_staff"),
    path("sis/export/staff/classes/<int:id>", admin_views.export_staff_enrolled_course, name="export_staff_enrolled_course"),
    path("sis/dashboard/", admin_views.dashboard, name="dashboard"),
    path("sis/gradebook", staff_views.gradebook, name="gradebook"),
    path("sis/gradebook/<int:course_id>/", staff_views.gradebook_course, name="gradebook_course"),
    path("sis/gradebook/report/<int:course_id>/<int:student_id>/", staff_views.gradebook_report, name="gradebook_report"),
    path("sis/gradebook/report/<int:course_id>/<int:student_id>/edit", staff_views.gradebook_report_edit, name="gradebook_report_edit"),


    # universal
    path("sis/inbox/", views.inbox, name="inbox"),
    path("sis/inbox_sent/", views.inbox_sent, name="inbox_sent"),
    path("sis/account/", views.account, name="account"),



]