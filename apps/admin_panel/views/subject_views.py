from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from apps.academic.models import Subject
from apps.admin_panel.decorators import admin_required
from apps.admin_panel.forms import SubjectForm

from apps.admin_panel.exports import export_to_excel, export_to_pdf


@admin_required
def subject_list(request):
    q = (request.GET.get("q") or "").strip()
    status = (request.GET.get("status") or "").strip()  # active / inactive / all(bo'sh)

    subjects = Subject.objects.all().order_by("name")

    if q:
        subjects = subjects.filter(
            Q(name__icontains=q) |
            Q(code__icontains=q)
        )

    if status == "active":
        subjects = subjects.filter(is_active=True)
    elif status == "inactive":
        subjects = subjects.filter(is_active=False)

    paginator = Paginator(subjects, per_page=15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")
    qs = query_params.urlencode()

    return render(
        request,
        "admin_panel/subjects/subject_list.html",
        {
            "subjects": page_obj,
            "count": subjects.count(),
            "filters": {
                "q": q,
                "status": status,
            },
            "page_obj": page_obj,
            "paginator": paginator,
            "is_paginated": page_obj.has_other_pages(),
            "qs": qs,
        },
    )


@admin_required
def subject_create(request):
    if request.method == "POST":
        form = SubjectForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fan muvaffaqiyatli qo‘shildi")
        else:
            # Show a clear warning message (first error) without breaking the flow
            first_error = None
            for errs in form.errors.values():
                if errs:
                    first_error = errs[0]
                    break
            messages.error(request, first_error or "Bu fan kodi allaqachon mavjud yoki ma’lumotlarda xatolik bor.")
    return redirect("admin_panel:subject_list")


@admin_required
def subject_update(request):
    if request.method == "POST":
        subject_id = request.POST.get("id")
        subject = get_object_or_404(Subject, id=subject_id)

        form = SubjectForm(data=request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Fan yangilandi")
        else:
            first_error = None
            for errs in form.errors.values():
                if errs:
                    first_error = errs[0]
                    break
            messages.error(request, first_error or "Bu fan kodi allaqachon mavjud yoki ma’lumotlarda xatolik bor.")

    return redirect("admin_panel:subject_list")


@admin_required
def subject_delete(request, id):
    subject = get_object_or_404(Subject, id=id)
    subject.delete()
    messages.success(request, "O‘chirildi")
    return redirect("admin_panel:subject_list")


@admin_required
@require_POST
def subject_toggle_status(request, id):
    subject = get_object_or_404(Subject, id=id)
    subject.is_active = not subject.is_active
    subject.save(update_fields=["is_active"])
    return JsonResponse({"is_active": subject.is_active})


@admin_required
def subjects_export_excel(request):
    headers = ["No", "Subject name", "Subject code", "Status", "Created date"]
    subjects = Subject.objects.all().order_by("name")
    rows = []
    for idx, s in enumerate(subjects, start=1):
        rows.append(
            [
                idx,
                s.name,
                s.code,
                "Active" if s.is_active else "Inactive",
                (s.created_at.date().isoformat() if getattr(s, "created_at", None) else ""),
            ]
        )

    return export_to_excel(
        filename="subjects.xlsx",
        headers=headers,
        rows=rows,
        sheet_title="Subjects",
    )


@admin_required
def subjects_export_pdf(request):
    headers = ["No", "Subject name", "Subject code", "Status", "Created date"]
    subjects = Subject.objects.all().order_by("name")
    rows = []
    for idx, s in enumerate(subjects, start=1):
        rows.append(
            [
                idx,
                s.name,
                s.code,
                "Active" if s.is_active else "Inactive",
                (s.created_at.date().isoformat() if getattr(s, "created_at", None) else ""),
            ]
        )

    return export_to_pdf(
        filename="subjects.pdf",
        title="Subjects",
        headers=headers,
        rows=rows,
    )
