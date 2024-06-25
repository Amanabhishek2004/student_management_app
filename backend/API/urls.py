from django.contrib import admin
from django.urls import path , include
from .views import *



urlpatterns = [
    path('students/' , StudentListCreateView.as_view() , name = "student-api"),
    path('assignmnets/' , AssignmentViewAPI.as_view() , name = "assignment-api" ),
    path('assignmnets/RUD/<int:pk>' , AssignmnetUpdateDestroyAPI.as_view() , name = "assignment-update-delete" ),
    path("given_assignments/" , AssignmentGivenDataAPI.as_view() , name="assignment-given-data"),
    path('Mark-Attendance/<int:pk>/' , MarkAttendanceAPI.as_view()  , name = "Mark-Attendance")
]