from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.core.exceptions import ValidationError
import re
from apps.admin_panel.decorators import admin_required
from apps.accounts.models import TeacherProfile, User
from django.db.models import Q
import re

from apps.admin_panel.exports import export_to_excel, export_to_pdf


@admin_required
def teacher_create(request):
    if request.method == "GET":
        return render(request, "admin_panel/teachers/teacher_create.html")

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        father_name = request.POST.get('father_name')
        birth_year = request.POST.get('birth_year') or None
        passport_id = (request.POST.get('passport_id') or '').strip().upper()
        jshshr = (request.POST.get('jshshr') or '').strip()
        photo = request.FILES.get('photo')
        username = (request.POST.get('username') or "").strip()
        password = request.POST.get('password')
        gender = request.POST.get('gender')

        # DB unique fieldlarda bo'sh string ('') qolib ketmasin
        passport_id = passport_id or None
        jshshr = jshshr or None

        # 1) Oldindan tekshiruvlar (user-friendly)
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' band. Boshqasini tanlang.")
            return render(request, "admin_panel/teachers/teacher_create.html", {
                "form": request.POST,
            })

        if passport_id and TeacherProfile.objects.filter(passport_id=passport_id).exists():
            messages.error(
                request,
                "Siz oldin bu teacherni yaratgansiz, iltimos qayta ma'lumotlarni ko'rib chiqing."
            )
            return render(request, "admin_panel/teachers/teacher_create.html", {
                "form": request.POST,
            })

        if jshshr and TeacherProfile.objects.filter(jshshr=jshshr).exists():
            messages.error(
                request,
                "Siz oldin bu teacherni yaratgansiz, iltimos qayta ma'lumotlarni ko'rib chiqing."
            )
            return render(request, "admin_panel/teachers/teacher_create.html", {
                "form": request.POST,
            })

        # Format tekshiruvi (DB ga bormasdan oldin) — aks holda varchar(14) DataError bo‘lishi mumkin
        if passport_id and not re.match(r"^[A-Z]{2}\d{7}$", passport_id):
            messages.error(request, "Passport formati: 2 ta katta harf + 7 ta raqam (masalan: AB1234567).")
            return render(request, "admin_panel/teachers/teacher_create.html", {
                "form": request.POST,
            })

        if jshshr and not re.match(r"^\d{14}$", jshshr):
            messages.error(request, "JSHSHR 14 ta raqamdan iborat bo‘lishi kerak.")
            return render(request, "admin_panel/teachers/teacher_create.html", {
                "form": request.POST,
            })

        subject = None


        # 2) Transaction: user yaratildi-yu, profil yaratilmadi degan holat bo‘lmasin
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    role='TEACHER',
                    is_active=True,
                )

                # full_clean() -> model validators (RegexValidator) va max_length kabi tekshiruvlar
                teacher = TeacherProfile(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    father_name=father_name,
                    birth_year=birth_year,
                    passport_id=passport_id,
                    jshshr=jshshr,
                    photo=photo,
                    gender=gender,
                    subject=subject,
                )
                teacher.full_clean()
                teacher.save()

            messages.success(request, "Yangi o‘qituvchi muvaffaqiyatli qo‘shildi ✅")
            return redirect("admin_panel:teacher_list")

        except IntegrityError:
            # baribir nimadir unique urilib qolsa
            messages.error(
                request,
                "Siz oldin bu teacherni yaratgansiz, iltimos qayta ma'lumotlarni ko'rib chiqing."
            )
            return render(request, "admin_panel/teachers/teacher_create.html", {
                "form": request.POST,
            })

        except DataError:
            messages.error(request, "Ma’lumot uzunligi noto‘g‘ri. Passport yoki JSHSHR formatini tekshiring.")
            return render(request, "admin_panel/teachers/teacher_create.html", {
                "form": request.POST,
            })

        except ValidationError as e:
            # Model validators (RegexValidator) xatolari
            error_messages = []
            if hasattr(e, 'message_dict'):
                for _, errs in e.message_dict.items():
                    error_messages.extend(errs)
            else:
                error_messages.append(str(e))

            for msg in error_messages:
                messages.error(request, msg)
            return render(request, "admin_panel/teachers/teacher_create.html", {
                "form": request.POST,
            })

    return redirect("admin_panel:teacher_list")

@admin_required
def teacher_list(request):
    q = request.GET.get("q", "").strip()
    name = request.GET.get("name", "").strip()
    passport = request.GET.get("passport", "").strip()
    jshshr = request.GET.get("jshshr", "").strip()
    birth_year = request.GET.get("birth_year", "").strip()
    gender = request.GET.get("gender", "").strip()
    status = request.GET.get("status", "").strip()

    teachers = TeacherProfile.objects.select_related('user', 'subject').all()

    # Umumiy qidiruv (action bar)
    if q:
        teachers = teachers.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(passport_id__icontains=q) |
            Q(jshshr__icontains=q)
        )

    # F.I.Sh bo‘yicha filtrlash
    if name:
        teachers = teachers.filter(
            Q(first_name__icontains=name) | Q(last_name__icontains=name)
        )

    # Passport bo‘yicha filtrlash
    if passport:
        teachers = teachers.filter(passport_id__icontains=passport)

    # JSHSHR bo‘yicha filtrlash
    if jshshr:
        teachers = teachers.filter(jshshr__icontains=jshshr)

    # Tug‘ilgan yili bo‘yicha filtrlash
    if birth_year:
        teachers = teachers.filter(birth_year=birth_year)

    # Jinsi bo‘yicha filtrlash
    if gender:
        teachers = teachers.filter(gender=gender)

    # Status bo‘yicha filtrlash (user is_active)
    if status == "active":
        teachers = teachers.filter(user__is_active=True)
    elif status == "inactive":
        teachers = teachers.filter(user__is_active=False)

    paginator = Paginator(teachers, per_page=15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")
    qs = query_params.urlencode()

    context = {
        'teachers': page_obj,
        'teacher_count': teachers.count(),
        'filters': {
            'q': q,
            'name': name,
            'passport': passport,
            'jshshr': jshshr,
            'birth_year': birth_year,
            'gender': gender,
            'status': status,
        },
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'qs': qs,
    }
    return render(request, 'admin_panel/teachers/teacher_list.html', context)


@admin_required
def teacher_update(request):
    if request.method == "POST":
        teacher = TeacherProfile.objects.select_related("user").get(
            id=request.POST.get("teacher_id")
        )

        # Asosiy ma’lumotlar
        teacher.first_name = request.POST.get("first_name")
        teacher.last_name = request.POST.get("last_name")
        teacher.birth_year = request.POST.get("birth_year") or None
        teacher.gender = request.POST.get("gender")

        # STATUS
        teacher.user.is_active = request.POST.get("is_active") == "1"
        teacher.user.save(update_fields=["is_active"])



        teacher.save()

        # 🔐 YANGI PAROL (ENG MUHIM)
        new_password = request.POST.get("new_password")
        if new_password:
            teacher.user.set_password(new_password)

        teacher.user.save()
        teacher.save()


        return redirect("admin_panel:teacher_list")


@admin_required
def teacher_delete(request, id):
    teacher = TeacherProfile.objects.select_related("user").get(id=id)
    teacher.user.delete()  # cascade bilan profile ham o‘chadi
    return redirect("admin_panel:teacher_list")

@admin_required
def teacher_toggle_status(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    teacher = TeacherProfile.objects.select_related("user").get(id=id)
    teacher.user.is_active = not teacher.user.is_active
    teacher.user.save(update_fields=["is_active"])

    return JsonResponse(
        {
            "success": True,
            "new_status": "active" if teacher.user.is_active else "inactive",
        }
    )


@admin_required
def teacher_export_excel(request):
    headers = [
        "No",
        "First name",
        "Last name",
        "Username",
        "Passport ID",
        "JSHSHR",
        "Phone",
        "Birth year",
        "Gender",
        "Status",
        "Created date",
    ]

    teachers = TeacherProfile.objects.select_related("user").all().order_by("last_name", "first_name")
    rows = []
    for idx, t in enumerate(teachers, start=1):
        u = t.user

        gender = "—"
        if t.gender == "male":
            gender = "Erkak"
        elif t.gender == "female":
            gender = "Ayol"

        # Phone is not currently stored in TeacherProfile/User in this project.
        phone_number = ""

        rows.append(
            [
                idx,
                t.first_name or "",
                t.last_name or "",
                u.username or "",
                t.passport_id or "",
                t.jshshr or "",
                phone_number,
                t.birth_year or "",
                gender,
                "Active" if u.is_active else "Inactive",
                (u.date_joined.date().isoformat() if getattr(u, "date_joined", None) else ""),
            ]
        )

    return export_to_excel(
        filename="teachers.xlsx",
        headers=headers,
        rows=rows,
        sheet_title="Teachers",
    )


@admin_required
def teacher_export_pdf(request):
    from reportlab.lib.pagesizes import A4, landscape

    headers = [
        "No",
        "First name",
        "Last name",
        "Username",
        "Passport ID",
        "JSHSHR",
        "Phone",
        "Birth year",
        "Gender",
        "Status",
        "Created date",
    ]

    teachers = TeacherProfile.objects.select_related("user").all().order_by("last_name", "first_name")
    rows = []
    for idx, t in enumerate(teachers, start=1):
        u = t.user

        gender = "—"
        if t.gender == "male":
            gender = "Erkak"
        elif t.gender == "female":
            gender = "Ayol"

        phone_number = ""

        rows.append(
            [
                idx,
                t.first_name or "",
                t.last_name or "",
                u.username or "",
                t.passport_id or "",
                t.jshshr or "",
                phone_number,
                t.birth_year or "",
                gender,
                "Active" if u.is_active else "Inactive",
                (u.date_joined.date().isoformat() if getattr(u, "date_joined", None) else ""),
            ]
        )

    return export_to_pdf(
        filename="teachers.pdf",
        title="Teachers",
        headers=headers,
        rows=rows,
        pagesize=landscape(A4),
    )




