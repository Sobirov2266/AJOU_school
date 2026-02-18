# apps/admin_panel/views/class_subject_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator

from apps.admin_panel.decorators import admin_required
from apps.academic.models import ClassSubject, SchoolClass, Subject
from apps.accounts.models import TeacherProfile

from apps.admin_panel.exports import export_to_excel, export_to_pdf


@admin_required
def class_subject_list(request):
    q = (request.GET.get("q") or "").strip()
    class_id = request.GET.get("class_id") or ""
    subject_id = request.GET.get("subject_id") or ""
    teacher_id = request.GET.get("teacher_id") or ""
    status = request.GET.get("status") or ""  # active / inactive / all(bo'sh)

    items = (
        ClassSubject.objects
        .select_related("school_class", "subject", "teacher", "teacher__user")
        .annotate(
            student_count=Count(
                "school_class__enrollments",
                filter=Q(school_class__enrollments__is_active=True),  # faqat active o‘quvchi
                distinct=True
            )
        )
        .all()
        .order_by("school_class__name", "subject__name")
    )

    if q:
        items = items.filter(
            Q(school_class__name__icontains=q) |
            Q(subject__name__icontains=q) |
            Q(subject__code__icontains=q) |
            Q(teacher__first_name__icontains=q) |
            Q(teacher__last_name__icontains=q)
        )

    if class_id:
        items = items.filter(school_class_id=class_id)

    if subject_id:
        items = items.filter(subject_id=subject_id)

    if teacher_id:
        items = items.filter(teacher_id=teacher_id)

    if status == "active":
        items = items.filter(is_active=True)
    elif status == "inactive":
        items = items.filter(is_active=False)

    paginator = Paginator(items, per_page=15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")
    qs = query_params.urlencode()

    classes = SchoolClass.objects.order_by("name")
    subjects = Subject.objects.filter(is_active=True).order_by("name")
    teachers = TeacherProfile.objects.select_related("user", "subject").order_by("last_name", "first_name")

    context = {
        "items": page_obj,
        "count": items.count(),
        "classes": classes,
        "subjects": subjects,
        "teachers": teachers,
        "filters": {
            "q": q,
            "class_id": class_id,
            "subject_id": subject_id,
            "teacher_id": teacher_id,
            "status": status,
        },
        "page_obj": page_obj,
        "paginator": paginator,
        "is_paginated": page_obj.has_other_pages(),
        "qs": qs,
        "q": q,
        "class_id": class_id,
        "subject_id": subject_id,
        "teacher_id": teacher_id,
        "status": status,
    }
    return render(request, "admin_panel/class_subjects/class_subject_list.html", context)


@admin_required
def class_subject_create(request):
    if request.method == "POST":
        school_class_id = request.POST.get("school_class")
        subject_id = request.POST.get("subject")
        teacher_id = request.POST.get("teacher") or None
        weekly_hours = request.POST.get("weekly_hours") or 0
        is_active = request.POST.get("is_active") == "1"

        if not school_class_id or not subject_id:
            messages.error(request, "Sinf va fan majburiy.")
            return redirect("admin_panel:class_subject_list")

        # Duplicate prevention (backend): do not allow identical combinations.
        # Uniqueness here is treated as (school_class, subject, teacher) where teacher can be NULL.
        exists_qs = ClassSubject.objects.filter(
            school_class_id=school_class_id,
            subject_id=subject_id,
        )
        if teacher_id:
            exists_qs = exists_qs.filter(teacher_id=teacher_id)
        else:
            exists_qs = exists_qs.filter(teacher__isnull=True)

        exists = exists_qs.exists()
        if exists:
            messages.error(request, "Bu sinfga ushbu fan allaqachon biriktirilgan.")
            return redirect("admin_panel:class_subject_list")

        ClassSubject.objects.create(
            school_class_id=school_class_id,
            subject_id=subject_id,
            teacher_id=teacher_id,
            weekly_hours=int(weekly_hours),
            is_active=is_active
        )
        messages.success(request, "Sinf fani muvaffaqiyatli qo‘shildi.")
        return redirect("admin_panel:class_subject_list")

    return redirect("admin_panel:class_subject_list")


@admin_required
def class_subject_update(request):
    if request.method == "POST":
        cs_id = request.POST.get("id")
        obj = get_object_or_404(ClassSubject, id=cs_id)

        school_class_id = request.POST.get("school_class")
        subject_id = request.POST.get("subject")
        teacher_id = request.POST.get("teacher") or None
        weekly_hours = request.POST.get("weekly_hours") or 0
        is_active = request.POST.get("is_active") == "1"

        if not school_class_id or not subject_id:
            messages.error(request, "Sinf va fan majburiy.")
            return redirect("admin_panel:class_subject_list")

        # Duplicate prevention (backend): prevent identical combinations excluding self.
        conflict_qs = ClassSubject.objects.filter(
            school_class_id=school_class_id,
            subject_id=subject_id,
        ).exclude(id=obj.id)
        if teacher_id:
            conflict_qs = conflict_qs.filter(teacher_id=teacher_id)
        else:
            conflict_qs = conflict_qs.filter(teacher__isnull=True)

        conflict = conflict_qs.exists()
        if conflict:
            messages.error(request, "Bu sinfga ushbu fan allaqachon biriktirilgan.")
            return redirect("admin_panel:class_subject_list")

        obj.school_class_id = school_class_id
        obj.subject_id = subject_id
        obj.teacher_id = teacher_id
        obj.weekly_hours = int(weekly_hours)
        obj.is_active = is_active
        obj.save()

        messages.success(request, "Sinf fani yangilandi.")
        return redirect("admin_panel:class_subject_list")

    return redirect("admin_panel:class_subject_list")


@admin_required
def class_subject_delete(request, id):
    obj = get_object_or_404(ClassSubject, id=id)
    obj.delete()
    messages.success(request, "O‘chirildi.")
    return redirect("admin_panel:class_subject_list")


@admin_required
@require_POST
def class_subject_toggle_status(request, id):
    obj = get_object_or_404(ClassSubject, id=id)
    obj.is_active = not obj.is_active
    obj.save(update_fields=["is_active"])
    return JsonResponse({"is_active": obj.is_active})


@admin_required
def class_subjects_export_excel(request):
    headers = [
        "No",
        "Class name",
        "Subject name",
        "Subject code",
        "Teacher name",
        "Status",
        "Created date",
    ]

    items = ClassSubject.objects.select_related(
        "school_class", "subject", "teacher", "teacher__user"
    ).order_by("school_class__name", "subject__name")

    rows = []
    for idx, cs in enumerate(items, start=1):
        teacher_name = ""
        if cs.teacher_id and cs.teacher:
            teacher_name = f"{cs.teacher.last_name or ''} {cs.teacher.first_name or ''}".strip()

        rows.append(
            [
                idx,
                cs.school_class.name if cs.school_class else "",
                cs.subject.name if cs.subject else "",
                cs.subject.code if cs.subject else "",
                teacher_name,
                "Active" if cs.is_active else "Inactive",
                (cs.created_at.date().isoformat() if getattr(cs, "created_at", None) else ""),
            ]
        )

    return export_to_excel(
        filename="class_subjects.xlsx",
        headers=headers,
        rows=rows,
        sheet_title="Class Subjects",
    )


@admin_required
def class_subjects_export_pdf(request):
    headers = [
        "No",
        "Class name",
        "Subject name",
        "Subject code",
        "Teacher name",
        "Status",
        "Created date",
    ]

    items = ClassSubject.objects.select_related(
        "school_class", "subject", "teacher", "teacher__user"
    ).order_by("school_class__name", "subject__name")

    rows = []
    for idx, cs in enumerate(items, start=1):
        teacher_name = ""
        if cs.teacher_id and cs.teacher:
            teacher_name = f"{cs.teacher.last_name or ''} {cs.teacher.first_name or ''}".strip()

        rows.append(
            [
                idx,
                cs.school_class.name if cs.school_class else "",
                cs.subject.name if cs.subject else "",
                cs.subject.code if cs.subject else "",
                teacher_name,
                "Active" if cs.is_active else "Inactive",
                (cs.created_at.date().isoformat() if getattr(cs, "created_at", None) else ""),
            ]
        )

    return export_to_pdf(
        filename="class_subjects.pdf",
        title="Class Subjects",
        headers=headers,
        rows=rows,
    )
