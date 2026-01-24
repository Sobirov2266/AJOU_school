from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.core.decorators import role_required
from apps.accounts.models import User, TeacherProfile
from apps.academic.models import SchoolClass


# ==========================
# TEACHER DASHBOARD
# ==========================
@login_required
@role_required([User.Role.TEACHER])
def teacher_dashboard(request):
    teacher_profile = TeacherProfile.objects.get(user=request.user)

    total_classes = SchoolClass.objects.filter(teacher=teacher_profile).count()

    context = {
        "total_students": 142,   # keyin dinamik qilamiz
        "total_courses": total_classes,
    }

    return render(request, "dashboard/teacher_dashboard.html", context)


# ==========================
# MY CLASSES (MENING SINFLARIM)
# ==========================
@login_required
@role_required([User.Role.TEACHER])
def my_classes(request):
    print("USERNAME =", request.user.username)
    print("ROLE =", request.user.role)

    teacher_profile = TeacherProfile.objects.filter(user=request.user).first()
    print("TEACHER_PROFILE =", teacher_profile)

    classes = SchoolClass.objects.filter(teacher=teacher_profile)

    return render(request, "dashboard/my_classes.html", {
        "classes": classes
    })


# ==========================
# STUDENT DASHBOARD
# ==========================
@login_required
@role_required([User.Role.STUDENT])
def student_dashboard(request):
    return render(request, "dashboard/student_dashboard.html")
