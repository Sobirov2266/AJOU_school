from django.shortcuts import render, redirect
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.urls import reverse
from apps.admin_panel.decorators import admin_required
from apps.accounts.models import TeacherProfile, User
from apps.academic.models import Subject
from django.db.models import Q


@admin_required
def teacher_create(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        father_name = request.POST.get('father_name')
        birth_year = request.POST.get('birth_year') or None
        passport_id = request.POST.get('passport_id')
        jshshr = request.POST.get('jshshr')
        username = (request.POST.get('username') or "").strip()
        password = request.POST.get('password')
        gender = request.POST.get('gender')

        # 1) Oldindan tekshiruvlar (user-friendly)
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' band. Boshqasini tanlang.")
            return redirect(reverse("admin_panel:teacher_list") + "?open=create")

        if TeacherProfile.objects.filter(passport_id=passport_id).exists():
            messages.error(request, f"Passport/ID '{passport_id}' allaqachon mavjud.")
            return redirect(reverse("admin_panel:teacher_list") + "?open=create")

        if TeacherProfile.objects.filter(jshshr=jshshr).exists():
            messages.error(request, f"JSHSHR '{jshshr}' allaqachon mavjud.")
            return redirect(reverse("admin_panel:teacher_list") + "?open=create")

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

                TeacherProfile.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    father_name=father_name,
                    birth_year=birth_year,
                    passport_id=passport_id,
                    jshshr=jshshr,
                    gender=gender,
                    subject=subject
                )

            messages.success(request, "Yangi o‘qituvchi muvaffaqiyatli qo‘shildi ✅")
            return redirect("admin_panel:teacher_list")

        except IntegrityError:
            # baribir nimadir unique urilib qolsa
            messages.error(request, "Saqlashda xatolik: username/passport/jshshr takrorlanib qoldi.")
            return redirect(reverse("admin_panel:teacher_list") + "?open=create")

    return redirect("admin_panel:teacher_list")

@admin_required
def teacher_list(request):
    q = request.GET.get("q", "").strip()
    teachers = TeacherProfile.objects.select_related('user', 'subject').all()
    teacher_count = TeacherProfile.objects.count()
    subjects = Subject.objects.all()

    if q:
        teachers = teachers.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(passport_id__icontains=q) |
            Q(jshshr__icontains=q)
        )

    teacher_count = teachers.count()

    context = {
        'teachers': teachers,
        'teacher_count': teacher_count,

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
    teacher = TeacherProfile.objects.select_related("user").get(id=id)
    teacher.user.is_active = not teacher.user.is_active
    teacher.user.save()
    return redirect("admin_panel:teacher_list")




