from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.accounts.models import StudentProfile
from apps.academic.models import Enrollment, SchoolClass
from django.utils.timezone import now
from django.contrib import messages
from apps.admin_panel.decorators import admin_required
from django.contrib.auth import get_user_model


User = get_user_model()
@admin_required
def student_list(request):
    students = (
        StudentProfile.objects
        .select_related('user')
        .prefetch_related('enrollment__school_class')
    )

    total_students = students.count()
    active_students = students.filter(enrollment__is_active=True).count()
    inactive_students = total_students - active_students
    today_students = students.filter(created_at__date=now().date()).count()

    return render(request, 'admin_panel/students/student_list.html', {
        'students': students,
        'total_students': total_students,
        'active_students': active_students,
        'inactive_students': inactive_students,
        'today_students': today_students,
    })


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
def toggle_student_status(request, enrollment_id):
    enrollment = Enrollment.objects.get(id=enrollment_id)
    enrollment.is_active = not enrollment.is_active
    enrollment.save()

    return JsonResponse({
        'is_active': enrollment.is_active
    })



@admin_required
def student_create(request):
    classes = SchoolClass.objects.all()   # ✅ GET uchun

    if request.method == "POST":
        # 1️⃣ USER MA'LUMOTLARI
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 2️⃣ STUDENT MA'LUMOTLARI
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        birth_date = request.POST.get("birth_date") or None
        passport_id = request.POST.get("passport_id")
        parent_phone = request.POST.get("parent_phone")
        avatar = request.FILES.get("avatar")
        class_id = request.POST.get("school_class")

        # 3️⃣ USER YARATISH
        user = User.objects.create_user(
            username=username,
            password=password,
            role="STUDENT",
            is_active=True
        )

        # 4️⃣ STUDENT PROFILE (MUHIM!)
        student = StudentProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            passport_id=passport_id,
            parent_phone=parent_phone,
            avatar=avatar
        )

        # 5️⃣ SINFGA BIRIKTIRISH
        if class_id:
            school_class = SchoolClass.objects.get(id=class_id)
            Enrollment.objects.create(
                student=student,
                school_class=school_class,
                is_active=True
            )

        messages.success(request, "Yangi o‘quvchi muvaffaqiyatli qo‘shildi")
        return redirect("admin_panel:admin_students")

    return render(
        request,
        "admin_panel/students/student_create.html",
        {
            "classes": classes   # ✅ template uchun
        }
    )


@require_POST
def student_delete(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    user = student.user

    student.delete()
    user.delete()

    return JsonResponse({"success": True})

