from django.urls import path

from .views.dashboard_views  import dashboard_view
from .views.profile_views    import profile_view
from .views.timetable_views  import timetable_view
from .views.attendance_views import attendance_list_view
from .views.grade_views      import grade_list_view


app_name = "student_panel"

urlpatterns = [
    path("dashboard/",   dashboard_view,       name="dashboard"),
    path("profile/",     profile_view,         name="profile"),
    path("timetable/",   timetable_view,       name="timetable"),
    path("attendance/",  attendance_list_view, name="attendance_list"),
    path("grades/",      grade_list_view,      name="grade_list"),
]
