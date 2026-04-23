from collections import OrderedDict
from datetime import datetime

from django.contrib import messages
from django.shortcuts import render

from ..decorators import teacher_required
from ...academic.models import Timetable


@teacher_required
def timetable_view(request):
    teacher_profile = getattr(request.user, "teacher_profile", None)

    if teacher_profile is None:
        messages.error(request, "Teacher profili topilmadi.")
        return render(
            request,
            "teacher_panel/timetable/timetable.html",
            {
                "timetables": [],
                "grouped_timetable": OrderedDict(),
                "today_code": "",
                "weekly_lessons_count": 0,
                "active_days_count": 0,
                "class_count": 0,
            },
        )

    timetables = (
        Timetable.objects
        .select_related(
            "class_subject",
            "class_subject__school_class",
            "class_subject__subject",
            "class_subject__teacher",
            "class_subject__teacher__user",
        )
        .filter(
            class_subject__teacher=teacher_profile,
            is_active=True,
            class_subject__is_active=True,
            class_subject__subject__is_active=True,
            class_subject__school_class__is_active=True,
        )
        .order_by("weekday", "lesson_order", "start_time")
    )

    grouped_timetable = OrderedDict()
    for day_code, day_name in Timetable.WEEKDAY_CHOICES:
        grouped_timetable[day_code] = {
            "label": day_name,
            "lessons": [],
        }

    for item in timetables:
        grouped_timetable[item.weekday]["lessons"].append(item)

    weekday_map = {
        0: "MON",
        1: "TUE",
        2: "WED",
        3: "THU",
        4: "FRI",
        5: "SAT",
        6: "SUN",
    }
    today_code = weekday_map.get(datetime.today().weekday(), "")

    weekly_lessons_count = timetables.count()
    active_days_count = sum(1 for _, data in grouped_timetable.items() if data["lessons"])
    class_count = len(
        set(item.class_subject.school_class_id for item in timetables)
    )

    context = {
        "timetables": timetables,
        "grouped_timetable": grouped_timetable,
        "today_code": today_code,
        "weekly_lessons_count": weekly_lessons_count,
        "active_days_count": active_days_count,
        "class_count": class_count,
    }
    return render(request, "teacher_panel/timetable/timetable.html", context)