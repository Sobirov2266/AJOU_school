from django.urls import path
from .views.dashboard_views import dashboard_view
from .views.subject_views import subject_list_view
from .views.attendance_views import attendance_list_view, attendance_mark_view
from .views.grade_views import grade_enter_view
from .views.assignment_views import assignment_list_view, assignment_create_view, assignment_detail_view
from .views.test_views import test_view
from .views.settings_views import settings_view
from .views.timetable_views import timetable_view


app_name = "teacher_panel"

urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("subjects/", subject_list_view, name="subject_list"),
    path("timetable/", timetable_view, name="timetable"),
    path("grades/enter/", grade_enter_view, name="grade_enter"),

    path("assignments/", assignment_list_view, name="assignment_list"),
    path("assignments/create/", assignment_create_view, name="assignment_create"),
    path("assignments/<int:pk>/", assignment_detail_view, name="assignment_detail"),

    path("testing/", test_view, name="test_list"),

    # Davomat — yangi
    path("attendance/", attendance_list_view, name="attendance_list"),
    path("attendance/<int:class_subject_id>/mark/", attendance_mark_view, name="attendance_mark"),

    path("settings/", settings_view, name="teacher_settings"),
]
