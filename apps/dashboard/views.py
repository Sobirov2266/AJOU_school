from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.core.decorators import role_required
from apps.accounts.models import User, TeacherProfile
from apps.academic.models import  ClassSubject


# ==========================
# TEACHER DASHBOARD
# ==========================
@login_required
@role_required([User.Role.TEACHER])
def teacher_dashboard(request):
    teacher_profile = TeacherProfile.objects.get(user=request.user)

    from apps.academic.models import ClassSubject

    total_classes = ClassSubject.objects.filter(
        teacher=teacher_profile,
        is_active=True
    ).values('school_class').distinct().count()

    context = {
        "total_students": 142,   # keyin dinamik qilamiz
        "total_courses": total_classes,
    }

    return render(request, "dashboard/teacher_dashboard.html", context)


# ==========================
# MY CLASSES (MENING FANFLARIM)
# ==========================
@login_required
def my_subjects(request):
    teacher_profile = TeacherProfile.objects.get(user=request.user)

    class_subjects = ClassSubject.objects.filter(
        teacher=teacher_profile,
        is_active=True
    ).select_related('subject', 'school_class')

    for s in class_subjects:
        s.student_count = s.school_class.enrollments.filter(is_active=True).count()


    return render(
        request,
        'teacher/my_subjects.html',
        {
            'class_subjects': class_subjects
        }
    )

# ==========================
# STUDENT DASHBOARD
# ==========================
@login_required
@role_required([User.Role.STUDENT])
def student_dashboard(request):
    return render(request, "dashboard/student_dashboard.html")
