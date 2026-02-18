from django.shortcuts import render
from apps.accounts.models import TeacherProfile, StudentProfile
from apps.academic.models import SchoolClass, Subject
from apps.admin_panel.decorators import admin_required


@admin_required
def admin_dashboard(request):
    teacher_count = TeacherProfile.objects.count()
    student_count = StudentProfile.objects.count()
    class_count = SchoolClass.objects.count()
    subject_count = Subject.objects.count()

    return render(request, 'admin_panel/dashboard.html', {
        'teacher_count': teacher_count,
        'student_count': student_count,
        'class_count': class_count,
        'subject_count': subject_count,
    })
