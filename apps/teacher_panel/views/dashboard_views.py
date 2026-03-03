from django.shortcuts import render
from ..decorators import teacher_required
from ...accounts.models import TeacherProfile, StudentProfile
from ...academic.models import SchoolClass, Subject

@teacher_required
def dashboard_view(request):
    teacher_count = TeacherProfile.objects.count()
    student_count = StudentProfile.objects.count()
    class_count = SchoolClass.objects.count()
    subject_count = Subject.objects.count()

    return render(request, 'teacher_panel/dashboard.html', {
        'teacher_count': teacher_count,
        'student_count': student_count,
        'class_count': class_count,
        'subject_count': subject_count,
    })
