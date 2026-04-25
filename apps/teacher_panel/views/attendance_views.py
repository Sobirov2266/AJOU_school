from datetime import date as date_cls

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse

from ..decorators import teacher_required
from ...accounts.models import TeacherProfile, StudentProfile
from ...academic.models import ClassSubject, Enrollment, Attendance

import json


def _get_teacher(request):
    """Request userdan TeacherProfile olish."""
    return TeacherProfile.objects.select_related("user").get(user=request.user)


def _parse_date(date_str):
    """
    Stringdan date obyekti yasaydi.
    Agar date_str None yoki noto'g'ri format bo'lsa — bugungi sanani qaytaradi.
    """
    if not date_str:
        return timezone.localdate()
    try:
        return date_cls.fromisoformat(date_str)
    except (ValueError, TypeError):
        return timezone.localdate()


@teacher_required
def attendance_list_view(request):
    """
    O'qituvchiga biriktirilgan barcha sinf-fanlarni ko'rsatadi.
    O'qituvchi bu yerdan qaysi sinfda davomat belgilashni tanlaydi.
    """
    teacher = _get_teacher(request)

    class_subjects = (
        ClassSubject.objects
        .filter(teacher=teacher, is_active=True)
        .select_related("school_class", "subject")
        .order_by("school_class__name", "subject__name")
    )

    return render(request, "teacher_panel/attendance/attendance_list.html", {
        "class_subjects": class_subjects,
    })


@teacher_required
def attendance_mark_view(request, class_subject_id):
    """
    Tanlangan sinf-fan uchun davomat belgilash sahifasi.

    GET  — o'quvchilar ro'yxatini ko'rsatadi.
           ?date=YYYY-MM-DD parametri orqali sana tanlanadi (default: bugun).

    POST — davomatni saqlaydi.
           Content-Type: application/json  → AJAX orqali saqlash
           Content-Type: form              → oddiy form orqali saqlash (JS yo'q bo'lsa)
    """
    teacher = _get_teacher(request)

    # Faqat o'z class_subject ini ko'rsin
    try:
        class_subject = (
            ClassSubject.objects
            .select_related("school_class", "subject")
            .get(id=class_subject_id, teacher=teacher, is_active=True)
        )
    except ClassSubject.DoesNotExist:
        messages.error(request, "Bunday sinf-fan topilmadi yoki sizga tegishli emas.")
        return redirect("teacher_panel:attendance_list")

    # ---- Sanani aniqlash ----
    if request.method == "POST":
        # POST da sana body yoki GET parametridan kelishi mumkin
        date_str = request.GET.get("date") or request.POST.get("date")
    else:
        date_str = request.GET.get("date")

    selected_date = _parse_date(date_str)

    # ---- Bu sinfda o'qiyotgan faol o'quvchilar ----
    enrollments = (
        Enrollment.objects
        .filter(school_class=class_subject.school_class, is_active=True)
        .select_related("student")
        .order_by("student__last_name", "student__first_name")
    )
    students = [e.student for e in enrollments]

    # ================================================================
    # POST — davomatni saqlash
    # ================================================================
    if request.method == "POST":

        # --- AJAX (JSON) so'rov ---
        if request.content_type and "application/json" in request.content_type:
            try:
                body = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"success": False, "error": "JSON formati noto'g'ri."}, status=400)

            records = body.get("records", [])
            save_date = _parse_date(body.get("date"))

            for rec in records:
                student_id = rec.get("student_id")
                status     = rec.get("status", Attendance.Status.PRESENT)
                note       = rec.get("note") or ""

                # Noto'g'ri status bo'lsa o'tkazib yuboramiz
                if status not in Attendance.Status.values:
                    continue

                # Student mavjudligini tekshiramiz
                try:
                    student = StudentProfile.objects.get(id=student_id)
                except StudentProfile.DoesNotExist:
                    continue

                Attendance.objects.update_or_create(
                    class_subject=class_subject,
                    student=student,
                    date=save_date,
                    defaults={"status": status, "note": note},
                )

            return JsonResponse({"success": True, "message": "Davomat saqlandi ✅"})

        # --- Oddiy form POST (JS yo'q bo'lsa) ---
        for student in students:
            status = request.POST.get(f"status_{student.id}", Attendance.Status.ABSENT)
            note   = request.POST.get(f"note_{student.id}", "")

            if status not in Attendance.Status.values:
                status = Attendance.Status.ABSENT

            Attendance.objects.update_or_create(
                class_subject=class_subject,
                student=student,
                date=selected_date,
                defaults={"status": status, "note": note},
            )

        messages.success(request, f"{selected_date} sanasi uchun davomat saqlandi ✅")
        return redirect(f"{request.path}?date={selected_date}")

    # ================================================================
    # GET — sahifani ko'rsatish
    # ================================================================

    # Tanlangan sana uchun mavjud davomat yozuvlarini olamiz
    existing_qs = Attendance.objects.filter(
        class_subject=class_subject,
        date=selected_date,
    ).select_related("student")

    # { student_id: Attendance } map — tez qidirish uchun
    existing_map = {a.student_id: a for a in existing_qs}

    # Har bir o'quvchi uchun holat va izohni birlashtirish
    student_rows = []
    for student in students:
        att = existing_map.get(student.id)   # None yoki Attendance obyekti
        student_rows.append({
            "student": student,
            "status":  att.status if att is not None else Attendance.Status.PRESENT,
            "note":    att.note   if att is not None else "",
            "saved":   att is not None,
        })

    # Statistika
    total         = len(student_rows)
    present_count = sum(1 for r in student_rows if r["status"] == Attendance.Status.PRESENT)
    absent_count  = sum(1 for r in student_rows if r["status"] == Attendance.Status.ABSENT)
    late_count    = sum(1 for r in student_rows if r["status"] == Attendance.Status.LATE)

    return render(request, "teacher_panel/attendance/attendance_mark.html", {
        "class_subject":  class_subject,
        "selected_date":  selected_date,
        "today":          timezone.localdate(),
        "student_rows":   student_rows,
        "total":          total,
        "present_count":  present_count,
        "absent_count":   absent_count,
        "late_count":     late_count,
        "already_saved":  bool(existing_map),
    })
