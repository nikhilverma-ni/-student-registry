from django.urls import path
from home.views import *

urlpatterns = [
    path("", homePage, name="homePage"),
    path("students/", students, name="students"),
    path("addStudents/", addStudents, name="addStudents"),
    path("updateStudents/", updateStudentsPage, name="updateStudents"),
    path("delete_student/<str:student_email>/", delete_student, name="delete_student"),
    path("students/update/<str:student_email>/", update_student, name="update_student"),
    path("students_pagination/", students_pagination, name="student_pagination")
]
