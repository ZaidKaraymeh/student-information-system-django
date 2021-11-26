from django.urls import path, include
from .views import views
from .views import admin_views
urlpatterns = [
    path("", views.home, name="home" ),
    path("add_course", admin_views.add_course, name="add_course" ),
    path("view_courses", admin_views.view_courses, name="view_courses"),
    path("edit_course/<int:id>", admin_views.edit_course, name="edit_course"),
    path("delete_course/<int:id>", admin_views.delete_course, name="delete_course"),
    path("export/courses", admin_views.export_courses, name="export_courses"),
    path("course_dashboard/<int:id>/<int:instructor_id>", admin_views.course_dashboard, name="course_dashboard"),

    # STUDENT URLS
    path("add_student/", admin_views.add_student, name="add_student" ),
    path("view_students/", admin_views.view_students, name="view_students"),
    path("view_student_enrolled_courses/<int:id>", admin_views.view_student_enrolled_courses, name="view_student_enrolled_courses"),
    path("delete_student_enrolled/<slug:course_id>/<int:id>/", admin_views.delete_course_enrolled, name="delete_student_enrolled"),
    path("export/students", admin_views.export_students, name="export_students"),

    # STAFF URLS

    path("add_staff", admin_views.add_staff, name="add_staff" ),
    path("view_staff/", admin_views.view_staff, name="view_staff"),
    path("view_instructor_enrolled_courses/<int:id>", admin_views.view_instructor_enrolled_courses, name="view_instructor_enrolled_courses"),
    path("export/staff", admin_views.export_staff, name="export_staff"),
    path("export/staff/classes/<int:id>", admin_views.export_staff_enrolled_course, name="export_staff_enrolled_course"),

]