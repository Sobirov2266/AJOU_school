from django.urls import path
from .views.dashboard_views import admin_dashboard
from .views.teacher_views import (
    teacher_list, teacher_create,
    teacher_update, teacher_delete,
    teacher_toggle_status
)

from .views import student_views
from .views.student_views import (
    toggle_student_status,
    student_list,
    student_edit,
    student_delete
)
from .views.class_views import (
    class_list, class_create,
    class_update, class_delete,
    class_toggle_status
)

from .views.class_subject_views import (
    class_subject_list,
    class_subject_create,
    class_subject_update,
    class_subject_delete,
    class_subject_toggle_status,
)



app_name = "admin_panel"


urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path("teachers/", teacher_list, name="teacher_list"),
    path("teachers/create/", teacher_create, name="teacher_create"),
    path("teachers/update/", teacher_update, name="teacher_update"),
    path("teachers/delete/<int:id>/", teacher_delete, name="teacher_delete"),
    path("teachers/toggle-status/<int:id>/", teacher_toggle_status, name="teacher_toggle_status"),

    # Students
    path('students/', student_views.student_list, name='admin_students'),
    path(
        'students/toggle-status/<int:enrollment_id>/',
        toggle_student_status,
        name='toggle_student_status'
    ),
    path("students/<int:pk>/edit/", student_edit, name="student_edit"),
    path("students/<int:pk>/delete/", student_delete, name="student_delete"),
    path(
        "students/create/",
        student_views.student_create,
        name="student_create"
    ),


    path("classes/", class_list, name="class_list"),
    path("classes/create/", class_create, name="class_create"),
    path("classes/update/", class_update, name="class_update"),
    path("classes/delete/<int:id>/", class_delete, name="class_delete"),
    path("classes/toggle-status/<int:id>/", class_toggle_status, name="class_toggle_status"),

    # sinf+fan+teacher
    path("class-subjects/", class_subject_list, name="class_subject_list"),
    path("class-subjects/create/", class_subject_create, name="class_subject_create"),
    path("class-subjects/update/", class_subject_update, name="class_subject_update"),
    path("class-subjects/delete/<int:id>/", class_subject_delete, name="class_subject_delete"),
    path("class-subjects/toggle-status/<int:id>/", class_subject_toggle_status, name="class_subject_toggle_status"),


]


