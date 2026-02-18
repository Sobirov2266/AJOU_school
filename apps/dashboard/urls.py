from django.urls import path
from . import views


app_name = 'dashboard'



urlpatterns = [
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('my-subjects/', views.my_subjects, name='my_subjects'),
    path('student/', views.student_dashboard, name='student_dashboard'),
]
