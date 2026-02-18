from django.urls import path
from .views.dashboard_views import admin_dashboard
from .views.teacher_views import (
    teacher_list, teacher_create,
    teacher_update, teacher_delete,
    teacher_toggle_status,
    teacher_export_excel,
    teacher_export_pdf,
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
    class_toggle_status,
    class_students,
    class_students_export_excel,
    class_students_export_pdf,
    classes_export_excel,
    classes_export_pdf,
)

from .views.class_subject_views import (
    class_subject_list,
    class_subject_create,
    class_subject_update,
    class_subject_delete,
    class_subject_toggle_status,
    class_subjects_export_excel,
    class_subjects_export_pdf,
)

from .views.settings_views import admin_settings
from .views.subject_views import (
    subject_list,
    subject_create,
    subject_update,
    subject_delete,
    subject_toggle_status,
    subjects_export_excel,
    subjects_export_pdf,
)



app_name = "admin_panel"


urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('settings/', admin_settings, name='admin_settings'),
    path('subjects/', subject_list, name='subject_list'),
    path('subjects/create/', subject_create, name='subject_create'),
    path('subjects/update/', subject_update, name='subject_update'),
    path('subjects/delete/<int:id>/', subject_delete, name='subject_delete'),
    path('subjects/toggle-status/<int:id>/', subject_toggle_status, name='subject_toggle_status'),
    path('subjects/export/excel/', subjects_export_excel, name='subjects_export_excel'),
    path('subjects/export/pdf/', subjects_export_pdf, name='subjects_export_pdf'),
    path("teachers/", teacher_list, name="teacher_list"),
    path("teachers/create/", teacher_create, name="teacher_create"),
    path("teachers/update/", teacher_update, name="teacher_update"),
    path("teachers/delete/<int:id>/", teacher_delete, name="teacher_delete"),
    path("teachers/toggle-status/<int:id>/", teacher_toggle_status, name="teacher_toggle_status"),
    path("teachers/export/excel/", teacher_export_excel, name="teacher_export_excel"),
    path("teachers/export/pdf/", teacher_export_pdf, name="teacher_export_pdf"),

    # Students
    path('students/', student_views.student_list, name='admin_students'),
    path('students/export/excel/', student_views.students_export_excel, name='students_export_excel'),
    path('students/export/pdf/', student_views.students_export_pdf, name='students_export_pdf'),
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
    path("classes/export/excel/", classes_export_excel, name="classes_export_excel"),
    path("classes/export/pdf/", classes_export_pdf, name="classes_export_pdf"),
    path("classes/<int:id>/students/", class_students, name="class_students"),
    path(
        "classes/<int:id>/students/export/excel/",
        class_students_export_excel,
        name="class_students_export_excel",
    ),
    path(
        "classes/<int:id>/students/export/pdf/",
        class_students_export_pdf,
        name="class_students_export_pdf",
    ),
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
    path("class-subjects/export/excel/", class_subjects_export_excel, name="class_subjects_export_excel"),
    path("class-subjects/export/pdf/", class_subjects_export_pdf, name="class_subjects_export_pdf"),


]


