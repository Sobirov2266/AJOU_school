from django.urls import path
from .views.dashboard_views import dashboard_view
from .views.subject_views import subject_list_view
from .views.attendance_views import attendance_mark_view
from .views.grade_views import grade_enter_view
from .views.assignment_views import assignments_list_view
from .views.test_views import test_view
from .views.settings_views import settings_view


app_name = "teacher_panel"

urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("subjects/", subject_list_view, name="subject_list"),
    path("grades/enter/", grade_enter_view, name="grade_enter"),
    path("assignments/", assignments_list_view, name="assignments_list"),
    path("testing/", test_view, name="test_list"),
    path("attendance/mark/", attendance_mark_view, name="attendance_mark"),
    path("settings/", settings_view, name="teacher_settings"),
]