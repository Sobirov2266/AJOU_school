from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from apps.accounts.models import StudentProfile
from apps.academic.models import Enrollment, SchoolClass
from django.utils.timezone import now
from django.contrib import messages
from apps.admin_panel.decorators import admin_required
from django.contrib.auth import get_user_model
from django.db.models import Q

from apps.admin_panel.forms import StudentCreateForm

from apps.admin_panel.exports import export_to_excel, export_to_pdf


User = get_user_model()
@admin_required
def student_list(request):
    q = request.GET.get("q", "").strip()
    name = request.GET.get("name", "").strip()
    passport = request.GET.get("passport", "").strip()
    class_id = request.GET.get("class_id", "").strip()
    birth_date = request.GET.get("birth_date", "").strip()
    status = request.GET.get("status", "").strip()

    students = (
        StudentProfile.objects
        .select_related('user')
        .prefetch_related('enrollment__school_class')
        .all()
    )

    # Umumiy qidiruv (action bar)
    if q:
        students = students.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(passport_id__icontains=q)
        )

    # F.I.Sh bo‘yicha filtrlash
    if name:
        students = students.filter(
            Q(first_name__icontains=name) | Q(last_name__icontains=name)
        )

    # Passport bo‘yicha filtrlash
    if passport:
        students = students.filter(passport_id__icontains=passport)

    # Sinf bo‘yicha filtrlash
    if class_id:
        students = students.filter(enrollment__school_class_id=class_id)

    # Tug‘ilgan sana bo‘yicha (ixtiyoriy, dizayn uchun)
    if birth_date:
        students = students.filter(birth_date=birth_date)

    # Status bo‘yicha filtrlash (enrollment is_active)
    if status == "active":
        students = students.filter(enrollment__is_active=True)
    elif status == "inactive":
        students = students.filter(enrollment__is_active=False)

    paginator = Paginator(students, per_page=15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")
    qs = query_params.urlencode()

    total_students = students.count()
    classes = SchoolClass.objects.order_by('name')

    return render(request, 'admin_panel/students/student_list.html', {
        'students': page_obj,
        'total_students': total_students,
        'classes': classes,
        'filters': {
            'q': q,
            'name': name,
            'passport': passport,
            'class_id': class_id,
            'birth_date': birth_date,
            'status': status,
        },
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'qs': qs,
    })


@admin_required
def students_export_excel(request):
    headers = [
        "No",
        "First name",
        "Last name",
        "Username",
        "Passport ID",
        "Class name",
        "Phone",
        "Birth date",
        "Status",
        "Created date",
    ]

    students = (
        StudentProfile.objects.select_related("user")
        .select_related("enrollment__school_class")
        .all()
        .order_by("last_name", "first_name")
    )

    rows = []
    for idx, s in enumerate(students, start=1):
        cls_name = ""
        if getattr(s, "enrollment", None) and getattr(s.enrollment, "school_class", None):
            cls_name = s.enrollment.school_class.name

        status = "Active" if getattr(s, "enrollment", None) and s.enrollment.is_active else "Inactive"

        rows.append(
            [
                idx,
                s.first_name or "",
                s.last_name or "",
                (s.user.username if s.user else ""),
                s.passport_id or "",
                cls_name,
                s.parent_phone or "",
                (s.birth_date.isoformat() if getattr(s, "birth_date", None) else ""),
                status,
                (s.created_at.date().isoformat() if getattr(s, "created_at", None) else ""),
            ]
        )

    return export_to_excel(
        filename="students.xlsx",
        headers=headers,
        rows=rows,
        sheet_title="Students",
    )


@admin_required
def students_export_pdf(request):
    headers = [
        "No",
        "First name",
        "Last name",
        "Username",
        "Passport ID",
        "Class name",
        "Phone",
        "Birth date",
        "Status",
        "Created date",
    ]

    students = (
        StudentProfile.objects.select_related("user")
        .select_related("enrollment__school_class")
        .all()
        .order_by("last_name", "first_name")
    )

    rows = []
    for idx, s in enumerate(students, start=1):
        cls_name = ""
        if getattr(s, "enrollment", None) and getattr(s.enrollment, "school_class", None):
            cls_name = s.enrollment.school_class.name

        status = "Active" if getattr(s, "enrollment", None) and s.enrollment.is_active else "Inactive"

        rows.append(
            [
                idx,
                s.first_name or "",
                s.last_name or "",
                (s.user.username if s.user else ""),
                s.passport_id or "",
                cls_name,
                s.parent_phone or "",
                (s.birth_date.isoformat() if getattr(s, "birth_date", None) else ""),
                status,
                (s.created_at.date().isoformat() if getattr(s, "created_at", None) else ""),
            ]
        )

    return export_to_pdf(
        filename="students.pdf",
        title="Students",
        headers=headers,
        rows=rows,
    )


@admin_required
def student_detail(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)

    return render(
        request,
        'admin_panel/students/student_detail.html',
        {
            'student': student
        }
    )

@admin_required
def student_edit(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    enrollment = Enrollment.objects.filter(student=student).first()
    classes = SchoolClass.objects.all()

    if request.method == "POST":
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.passport_id = request.POST.get("passport_id")
        student.parent_phone = request.POST.get("parent_phone")

        class_id = request.POST.get("school_class")

        if class_id:
            school_class = get_object_or_404(SchoolClass, id=class_id)
            Enrollment.objects.update_or_create(
                student=student,
                defaults={
                    "school_class": school_class,
                    "is_active": True
                }
            )

        new_password = request.POST.get("new_password")
        if new_password:
            student.user.set_password(new_password)
            student.user.save()

        student.save()
        messages.success(request, "O‘quvchi ma’lumotlari yangilandi")
        return redirect("admin_panel:admin_students")

    return render(
        request,
        "admin_panel/students/student_edit.html",
        {
            "student": student,
            "enrollment": enrollment,
            "classes": classes,
        }
    )



@admin_required
@require_POST
def toggle_student_status(request, enrollment_id):
    enrollment = Enrollment.objects.get(id=enrollment_id)
    enrollment.is_active = not enrollment.is_active
    enrollment.save()

    return JsonResponse({
        'is_active': enrollment.is_active
    })



@admin_required
def student_create(request):
    classes = SchoolClass.objects.all()

    if request.method == "POST":
        form = StudentCreateForm(
            data=request.POST,
            files=request.FILES,
        )

        if form.is_valid():
            form.save(request=request)
            messages.success(request, "Yangi o‘quvchi muvaffaqiyatli qo‘shildi")
            return redirect("admin_panel:admin_students")

        # IMPORTANT: backend validation errors are shown in the same page
        # If duplicate student detected, show the exact required message.
        duplicate_msg = "Siz yaratgan talaba oldin yaratilgan, oldin tekshirib qayta ma'lumotlarni kiriting."
        passport_errors = form.errors.get("passport_id")
        if passport_errors and duplicate_msg in passport_errors:
            messages.error(request, duplicate_msg)
        else:
            first_error = None
            for errs in form.errors.values():
                if errs:
                    first_error = errs[0]
                    break
            messages.error(request, first_error or "Ma’lumotlarda xatolik bor. Iltimos, tekshirib qayta urinib ko‘ring.")
        return render(
            request,
            "admin_panel/students/student_create.html",
            {
                "classes": classes,
                "form": form,
            }
        )

    return render(
        request,
        "admin_panel/students/student_create.html",
        {
            "classes": classes,
            "form": None,
        }
    )


@admin_required
def student_delete(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    user = student.user

    student.delete()
    user.delete()

    return JsonResponse({"success": True})

