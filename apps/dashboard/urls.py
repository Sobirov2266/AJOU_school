from django.urls import path
from .views import teacher_dashboard, student_dashboard, my_classes

urlpatterns = [
    path('teacher/', teacher_dashboard, name='teacher_dashboard'),
    path('student/', student_dashboard, name='student_dashboard'),
    path("my-classes/", my_classes, name="my_classes"),
]
