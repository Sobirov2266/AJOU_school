from django.shortcuts import render
from django.utils import timezone

from ..decorators import student_required
from ...accounts.models import StudentProfile
from ...academic.models import Enrollment, Timetable, Attendance, Grade


def _get_student(request):
    """Request userdan StudentProfile olish."""
    return StudentProfile.objects.select_related("user").get(user=request.user)


@student_required
def dashboard_view(request):
    """
    Student dashboard sahifasi.
    Ko'rsatiladigan ma'lumotlar:
      - O'quvchining ismi va sinfi
      - Bugungi dars jadvali
      - Oxirgi 5 ta baho
      - Umumiy davomat foizi (joriy oy)
    """
    student = _get_student(request)

    # O'quvchining sinfi
    enrollment = getattr(student, "enrollment", None)
    school_class = enrollment.school_class if enrollment else None

    # Bugungi hafta kuni (MON, TUE, ...)
    weekday_map = {0: "MON", 1: "TUE", 2: "WED", 3: "THU", 4: "FRI", 5: "SAT", 6: "SUN"}
    today_weekday = weekday_map.get(timezone.localdate().weekday(), "")

    # Bugungi dars jadvali
    today_timetable = []
    if school_class:
        today_timetable = (
            Timetable.objects
            .filter(
                class_subject__school_class=school_class,
                weekday=today_weekday,
                is_active=True,
            )
            .select_related("class_subject__subject", "class_subject__teacher")
            .order_by("lesson_order")
        )

    # Oxirgi 5 ta baho
    recent_grades = (
        Grade.objects
        .filter(student=student)
        .select_related("class_subject__subject")
        .order_by("-date", "-created_at")[:5]
    )

    # Joriy oy davomati foizi
    today = timezone.localdate()
    month_start = today.replace(day=1)
    month_attendances = Attendance.objects.filter(
        student=student,
        date__gte=month_start,
        date__lte=today,
    )
    total_att = month_attendances.count()
    present_att = month_attendances.filter(status=Attendance.Status.PRESENT).count()
    attendance_percent = round((present_att / total_att) * 100) if total_att > 0 else None

    return render(request, "student_panel/dashboard.html", {
        "student":            student,
        "school_class":       school_class,
        "today_timetable":    today_timetable,
        "recent_grades":      recent_grades,
        "attendance_percent": attendance_percent,
        "present_att":        present_att,
        "total_att":          total_att,
        "today":              today,
        "today_weekday":      today_weekday,
    })
