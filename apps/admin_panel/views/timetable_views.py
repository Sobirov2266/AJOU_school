from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from datetime import time
from django.shortcuts import get_object_or_404

from ..decorators import admin_required
from ...academic.models import Timetable
from ..forms import TimetableForm


@admin_required
def timetable_list(request):
    q = (request.GET.get("q") or "").strip()
    weekday = (request.GET.get("weekday") or "").strip()
    status = (request.GET.get("status") or "").strip()

    timetables = (
        Timetable.objects
        .select_related(
            "class_subject",
            "class_subject__school_class",
            "class_subject__subject",
            "class_subject__teacher",
            "class_subject__teacher__user",
        )
        .order_by("weekday", "lesson_order", "start_time")
    )

    if q:
        timetables = timetables.filter(
            Q(class_subject__school_class__name__icontains=q) |
            Q(class_subject__subject__name__icontains=q) |
            Q(class_subject__subject__code__icontains=q) |
            Q(class_subject__teacher__first_name__icontains=q) |
            Q(class_subject__teacher__last_name__icontains=q) |
            Q(room__icontains=q)
        )

    if weekday:
        timetables = timetables.filter(weekday=weekday)

    if status == "active":
        timetables = timetables.filter(is_active=True)
    elif status == "inactive":
        timetables = timetables.filter(is_active=False)

    paginator = Paginator(timetables, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")
    qs = query_params.urlencode()

    return render(
        request,
        "admin_panel/timetable/timetable_list.html",
        {
            "timetables": page_obj,
            "timetable_count": timetables.count(),
            "page_obj": page_obj,
            "paginator": paginator,
            "is_paginated": page_obj.has_other_pages(),
            "qs": qs,
            "filters": {
                "q": q,
                "weekday": weekday,
                "status": status,
            },
            "weekday_choices": Timetable.WEEKDAY_CHOICES,
            "create_form": TimetableForm(),

        },
    )


@admin_required
def timetable_create(request):
    if request.method == "POST":
        form = TimetableForm(request.POST)
        if form.is_valid():
            timetable = form.save(commit=False)

            period_times = Timetable.get_period_times(timetable.lesson_order)
            if not period_times:
                messages.error(request, "Dars raqami uchun vaqt topilmadi.")
                return redirect("admin_panel:timetable_list")

            start_str, end_str = period_times
            start_hour, start_minute = map(int, start_str.split(":"))
            end_hour, end_minute = map(int, end_str.split(":"))

            timetable.start_time = time(start_hour, start_minute)
            timetable.end_time = time(end_hour, end_minute)

            timetable.save()
            messages.success(request, "Dars jadvali muvaffaqiyatli qo‘shildi.")
        else:
            first_error = None
            for errs in form.errors.values():
                if errs:
                    first_error = errs[0]
                    break
            messages.error(request, first_error or "Dars jadvalini saqlashda xatolik yuz berdi.")

    return redirect("admin_panel:timetable_list")


@admin_required
def timetable_update(request):
    if request.method == "POST":
        timetable_id = request.POST.get("id")
        timetable = get_object_or_404(Timetable, id=timetable_id)

        form = TimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            timetable = form.save(commit=False)

            period_times = Timetable.get_period_times(timetable.lesson_order)
            if not period_times:
                messages.error(request, "Dars raqami uchun vaqt topilmadi.")
                return redirect("admin_panel:timetable_list")

            start_str, end_str = period_times
            start_hour, start_minute = map(int, start_str.split(":"))
            end_hour, end_minute = map(int, end_str.split(":"))

            timetable.start_time = time(start_hour, start_minute)
            timetable.end_time = time(end_hour, end_minute)

            timetable.save()
            messages.success(request, "Dars jadvali muvaffaqiyatli yangilandi.")
        else:
            first_error = None
            for errs in form.errors.values():
                if errs:
                    first_error = errs[0]
                    break
            messages.error(request, first_error or "Dars jadvalini yangilashda xatolik yuz berdi.")

    return redirect("admin_panel:timetable_list")


@admin_required
def timetable_delete(request, id):
    timetable = get_object_or_404(Timetable, id=id)
    timetable.delete()
    messages.success(request, "Dars jadvali o‘chirildi.")
    return redirect("admin_panel:timetable_list")