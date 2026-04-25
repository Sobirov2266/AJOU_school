from django.shortcuts import render

from ..decorators import student_required
from ...accounts.models import StudentProfile
from ...academic.models import Enrollment, ClassSubject, Attendance


def _get_student(request):
    return StudentProfile.objects.select_related("user").get(user=request.user)


@student_required
def attendance_list_view(request):
    """
    O'quvchining barcha fanlar bo'yicha davomat statistikasi.
    Har bir fan uchun: jami darslar, keldi, kelmadi, kech keldi, foiz.
    """
    student = _get_student(request)
    enrollment = getattr(student, "enrollment", None)
    school_class = enrollment.school_class if enrollment else None

    subject_stats = []

    if school_class:
        # O'quvchi o'qiyotgan sinfning barcha faol sinf-fanlari
        class_subjects = (
            ClassSubject.objects
            .filter(school_class=school_class, is_active=True)
            .select_related("subject", "teacher")
            .order_by("subject__name")
        )

        for cs in class_subjects:
            # Bu sinf-fan uchun o'quvchining barcha davomati
            qs = Attendance.objects.filter(
                class_subject=cs,
                student=student,
            )
            total   = qs.count()
            present = qs.filter(status=Attendance.Status.PRESENT).count()
            absent  = qs.filter(status=Attendance.Status.ABSENT).count()
            late    = qs.filter(status=Attendance.Status.LATE).count()
            percent = round((present / total) * 100) if total > 0 else None

            subject_stats.append({
                "class_subject": cs,
                "total":         total,
                "present":       present,
                "absent":        absent,
                "late":          late,
                "percent":       percent,
            })

    # Umumiy statistika
    grand_total   = sum(s["total"]   for s in subject_stats)
    grand_present = sum(s["present"] for s in subject_stats)
    grand_absent  = sum(s["absent"]  for s in subject_stats)
    grand_late    = sum(s["late"]    for s in subject_stats)
    grand_percent = (
        round((grand_present / grand_total) * 100)
        if grand_total > 0 else None
    )

    return render(request, "student_panel/attendance/attendance_list.html", {
        "student":       student,
        "school_class":  school_class,
        "subject_stats": subject_stats,
        "grand_total":   grand_total,
        "grand_present": grand_present,
        "grand_absent":  grand_absent,
        "grand_late":    grand_late,
        "grand_percent": grand_percent,
    })
