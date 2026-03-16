from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages

from ..decorators import teacher_required
from ...academic.models import ClassSubject



@teacher_required
def subject_list_view(request):
    teacher_profile = getattr(request.user, "teacher_profile", None)

    if teacher_profile is None:
        messages.error(request, "Teacher profili topilmadi.")
        return render(
            request,
            "teacher_panel/subjects/subject_list.html",
            {
                "subjects": [],
                "subject_count": 0,
                "q": "",
                "page_obj": None,
                "paginator": None,
                "is_paginated": False,
                "qs": "",
            },
        )

    q = (request.GET.get("q") or "").strip()
    view_mode = (request.GET.get("view") or "").strip().lower() or "table"

    subjects = (
        ClassSubject.objects
        .select_related("school_class", "subject")
        .filter(
            teacher=teacher_profile,
            is_active=True,
            subject__is_active=True,
            school_class__is_active=True,
        )
        .annotate(
            student_count=Count(
                "school_class__enrollments",
                filter=Q(school_class__enrollments__is_active=True),
                distinct=True,
            )
        )
        .order_by("subject__name", "school_class__name")
    )

    if q:
        subjects = subjects.filter(
            Q(subject__name__icontains=q) |
            Q(subject__code__icontains=q) |
            Q(school_class__name__icontains=q)
        )

    paginator = Paginator(subjects, 12 if view_mode == "cards" else 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")
    qs = query_params.urlencode()



    return render(
        request,
        "teacher_panel/subjects/subject_list.html",
        {
            "subjects": page_obj,
            "subject_count": subjects.count(),
            "q": q,
            "page_obj": page_obj,
            "paginator": paginator,
            "is_paginated": page_obj.has_other_pages(),
            "qs": qs,
        },
    )