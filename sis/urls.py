from django.urls import path, include
from .views import views
from .views import admin_views
urlpatterns = [
    path("", views.home, name="home" ),
    path("add_student", admin_views.add_course, name="add_course" ),
    path("view_courses", admin_views.view_courses, name="view_courses"),
    path("edit_course/<int:id>", admin_views.edit_course, name="edit_course"),
]