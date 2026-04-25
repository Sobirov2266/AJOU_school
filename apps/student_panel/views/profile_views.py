from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from ..decorators import student_required
from ...accounts.models import StudentProfile


def _get_student(request):
    return StudentProfile.objects.select_related("user").get(user=request.user)


@student_required
def profile_view(request):
    """
    O'quvchining shaxsiy profil sahifasi.
    GET  → profilni ko'rsatadi
    POST → ma'lumotlarni yangilaydi (avatar, telefon)
    """
    student = _get_student(request)
    enrollment = getattr(student, "enrollment", None)

    if request.method == "POST":
        action = request.POST.get("action")

        # --- Profil ma'lumotlarini yangilash ---
        if action == "update_profile":
            parent_phone = request.POST.get("parent_phone", "").strip()
            if parent_phone:
                student.parent_phone = parent_phone

            # Avatar yuklash
            if "avatar" in request.FILES:
                # Eski avatarni o'chirish (ixtiyoriy)
                if student.avatar:
                    student.avatar.delete(save=False)
                student.avatar = request.FILES["avatar"]

            student.save()
            messages.success(request, "Profil ma'lumotlari yangilandi ✅")
            return redirect("student_panel:profile")

        # --- Parol o'zgartirish ---
        if action == "change_password":
            old_password    = request.POST.get("old_password", "")
            new_password    = request.POST.get("new_password", "")
            confirm_password = request.POST.get("confirm_password", "")

            user = request.user

            if not user.check_password(old_password):
                messages.error(request, "Eski parol noto'g'ri.")
                return redirect("student_panel:profile")

            if len(new_password) < 6:
                messages.error(request, "Yangi parol kamida 6 ta belgidan iborat bo'lishi kerak.")
                return redirect("student_panel:profile")

            if new_password != confirm_password:
                messages.error(request, "Yangi parollar mos kelmadi.")
                return redirect("student_panel:profile")

            user.set_password(new_password)
            user.must_change_password = False
            user.save()

            # Sessiyani yangilash — parol o'zgarganda logout bo'lmasin
            update_session_auth_hash(request, user)

            messages.success(request, "Parol muvaffaqiyatli o'zgartirildi ✅")
            return redirect("student_panel:profile")

    return render(request, "student_panel/profile.html", {
        "student":    student,
        "enrollment": enrollment,
    })
