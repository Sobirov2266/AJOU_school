from django.shortcuts import render

from ..decorators import student_required
from ...accounts.models import StudentProfile
from ...academic.models import Timetable


WEEKDAYS_ORDER = ["MON", "TUE", "WED", "THU", "FRI"]
WEEKDAYS_DISPLAY = {
    "MON": "Dushanba",
    "TUE": "Seshanba",
    "WED": "Chorshanba",
    "THU": "Payshanba",
    "FRI": "Juma",
}


def _get_student(request):
    return StudentProfile.objects.select_related("user").get(user=request.user)


@student_required
def timetable_view(request):
    """
    O'quvchining haftalik dars jadvali.
    Hafta kunlari bo'yicha guruhlanib ko'rsatiladi.
    """
    student = _get_student(request)
    enrollment = getattr(student, "enrollment", None)
    school_class = enrollment.school_class if enrollment else None

    # Haftalik jadval — har bir kun uchun darslar ro'yxati
    timetable_by_day = []

    if school_class:
        all_entries = (
            Timetable.objects
            .filter(
                class_subject__school_class=school_class,
                is_active=True,
            )
            .select_related(
                "class_subject__subject",
                "class_subject__teacher",
            )
            .order_by("weekday", "lesson_order")
        )

        # Kunlar bo'yicha guruhlash
        entries_by_day = {}
        for entry in all_entries:
            entries_by_day.setdefault(entry.weekday, []).append(entry)

        for day_code in WEEKDAYS_ORDER:
            timetable_by_day.append({
                "code":    day_code,
                "name":    WEEKDAYS_DISPLAY[day_code],
                "lessons": entries_by_day.get(day_code, []),
            })

    return render(request, "student_panel/timetable.html", {
        "student":         student,
        "school_class":    school_class,
        "timetable_by_day": timetable_by_day,
    })
