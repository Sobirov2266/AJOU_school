from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from apps.academic.models import Enrollment, SchoolClass
from apps.admin_panel.decorators import admin_required
from django.contrib import messages

from apps.admin_panel.exports import export_to_excel, export_to_pdf

from apps.admin_panel.forms import ClassNameForm

@admin_required
def class_list(request):
    q = request.GET.get("q", "").strip()
    view_mode = (request.GET.get("view") or "").strip().lower() or "table"
    per_page = 12 if view_mode == "cards" else 15

    classes = (
        SchoolClass.objects.all()
        .annotate(
            students_count=Count(
                "enrollments",
                filter=Q(enrollments__is_active=True),
            )
        )
        .order_by("name")
    )

    if q:
        classes = classes.filter(Q(name__icontains=q))

    paginator = Paginator(classes, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")
    qs = query_params.urlencode()

    return render(
        request,
        "admin_panel/classes/class_list.html",
        {
            "classes": page_obj,
            "class_count": classes.count(),
            "q": q,
            "page_obj": page_obj,
            "paginator": paginator,
            "is_paginated": page_obj.has_other_pages(),
            "qs": qs,
            "view_mode": view_mode,
        },
    )


@admin_required
def classes_export_excel(request):
    headers = ["No", "Class name", "Class ID", "Students count", "Status", "Created date"]
    classes = (
        SchoolClass.objects.all()
        .annotate(
            students_count=Count(
                "enrollments",
                filter=Q(enrollments__is_active=True),
            )
        )
        .order_by("name")
    )

    rows = []
    for idx, c in enumerate(classes, start=1):
        rows.append(
            [
                idx,
                c.name,
                c.id,
                getattr(c, "students_count", 0),
                "Active" if c.is_active else "Inactive",
                (c.created_at.date().isoformat() if getattr(c, "created_at", None) else ""),
            ]
        )

    return export_to_excel(
        filename="classes.xlsx",
        headers=headers,
        rows=rows,
        sheet_title="Classes",
    )


@admin_required
def classes_export_pdf(request):
    headers = ["No", "Class name", "Class ID", "Students count", "Status", "Created date"]
    classes = (
        SchoolClass.objects.all()
        .annotate(
            students_count=Count(
                "enrollments",
                filter=Q(enrollments__is_active=True),
            )
        )
        .order_by("name")
    )

    rows = []
    for idx, c in enumerate(classes, start=1):
        rows.append(
            [
                idx,
                c.name,
                c.id,
                getattr(c, "students_count", 0),
                "Active" if c.is_active else "Inactive",
                (c.created_at.date().isoformat() if getattr(c, "created_at", None) else ""),
            ]
        )

    return export_to_pdf(
        filename="classes.pdf",
        title="Classes",
        headers=headers,
        rows=rows,
    )


@admin_required
def class_students(request, id):
    school_class = get_object_or_404(SchoolClass, id=id)

    enrollments = (
        Enrollment.objects.filter(school_class=school_class, is_active=True)
        .select_related("student", "student__user")
        .order_by("student__last_name", "student__first_name")
    )

    return render(
        request,
        "admin_panel/classes/class_students.html",
        {
            "school_class": school_class,
            "enrollments": enrollments,
        },
    )


def _export_rows_for_class(school_class):
    enrollments = (
        Enrollment.objects.filter(school_class=school_class, is_active=True)
        .select_related("student", "student__user")
        .order_by("student__last_name", "student__first_name")
    )

    # Columns must be exactly:
    # 1. First name
    # 2. Last name
    # 3. Login
    # 4. Password (initial password = passport ID)
    rows = []
    for e in enrollments:
        student = e.student
        rows.append(
            (
                student.first_name,
                student.last_name,
                student.user.username,
                student.passport_id,
            )
        )
    return rows


@admin_required
def class_students_export_excel(request, id):
    school_class = get_object_or_404(SchoolClass, id=id)

    # Export logic (Excel) implemented here.
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = "Students"

    ws.append(["No", "First name", "Last name", "Login", "Password"])
    for idx, row in enumerate(_export_rows_for_class(school_class), start=1):
        ws.append([idx] + list(row))

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="class_{school_class.id}_students.xlsx"'
    wb.save(response)
    return response


@admin_required
def class_students_export_pdf(request, id):
    school_class = get_object_or_404(SchoolClass, id=id)

    # Export logic (PDF) implemented here.
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="class_{school_class.id}_students.pdf"'

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Class: {school_class.name}")
    y -= 30

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "No")
    c.drawString(85, y, "First name")
    c.drawString(200, y, "Last name")
    c.drawString(315, y, "Login")
    c.drawString(430, y, "Password")
    y -= 18
    c.setFont("Helvetica", 10)

    for idx, (first_name, last_name, login, password) in enumerate(_export_rows_for_class(school_class), start=1):
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)

        c.drawString(50, y, str(idx))
        c.drawString(85, y, str(first_name or ""))
        c.drawString(200, y, str(last_name or ""))
        c.drawString(315, y, str(login or ""))
        c.drawString(430, y, str(password or ""))
        y -= 16

    c.showPage()
    c.save()
    return response


@admin_required
def class_create(request):
    if request.method == "POST":
        form = ClassNameForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            SchoolClass.objects.create(name=name)
            messages.success(request, "Yangi sinf qo‘shildi")
        else:
            # IMPORTANT: keep behavior simple (modal page) and show a friendly message
            messages.error(request, form.errors.get("name", ["Sinf nomi noto‘g‘ri."])[0])
    return redirect("admin_panel:class_list")


@admin_required
def class_update(request):
    if request.method == "POST":
        class_id = request.POST.get("class_id")
        school_class = get_object_or_404(SchoolClass, id=class_id)

        form = ClassNameForm(data=request.POST, instance=school_class)
        if form.is_valid():
            school_class.name = form.cleaned_data["name"]
            school_class.is_active = (request.POST.get("is_active") == "1")
            school_class.save()
            messages.success(request, "Sinf yangilandi")
        else:
            messages.error(request, form.errors.get("name", ["Sinf nomi noto‘g‘ri."])[0])
    return redirect("admin_panel:class_list")


@admin_required
@require_POST
def class_delete(request, id):
    school_class = get_object_or_404(SchoolClass, id=id)
    school_class.delete()
    messages.success(request, "Sinf o‘chirildi")
    return redirect("admin_panel:class_list")


@admin_required
@require_POST
def class_toggle_status(request, id):
    school_class = get_object_or_404(SchoolClass, id=id)
    school_class.is_active = not school_class.is_active
    school_class.save(update_fields=["is_active"])
    return redirect("admin_panel:class_list")
