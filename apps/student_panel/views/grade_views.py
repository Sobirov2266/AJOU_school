from django.shortcuts import render

from ..decorators import student_required
from ...accounts.models import StudentProfile
from ...academic.models import ClassSubject, Grade


def _get_student(request):
    return StudentProfile.objects.select_related("user").get(user=request.user)


@student_required
def grade_list_view(request):
    """
    O'quvchining barcha fanlar bo'yicha baholari.
    Har bir fan uchun: joriy, oraliq, yakuniy baholar va o'rtacha.
    """
    student = _get_student(request)
    enrollment = getattr(student, "enrollment", None)
    school_class = enrollment.school_class if enrollment else None

    subject_grades = []

    if school_class:
        class_subjects = (
            ClassSubject.objects
            .filter(school_class=school_class, is_active=True)
            .select_related("subject", "teacher")
            .order_by("subject__name")
        )

        for cs in class_subjects:
            # Bu fan uchun o'quvchining barcha baholari
            grades_qs = (
                Grade.objects
                .filter(class_subject=cs, student=student)
                .order_by("date")
            )

            current_grades = [g for g in grades_qs if g.grade_type == Grade.GradeType.CURRENT]
            midterm_grades = [g for g in grades_qs if g.grade_type == Grade.GradeType.MIDTERM]
            final_grades   = [g for g in grades_qs if g.grade_type == Grade.GradeType.FINAL]

            all_values = [g.value for g in grades_qs]
            average = round(sum(all_values) / len(all_values), 1) if all_values else None

            subject_grades.append({
                "class_subject":  cs,
                "current_grades": current_grades,
                "midterm_grades": midterm_grades,
                "final_grades":   final_grades,
                "average":        average,
                "total_count":    len(all_values),
            })

    return render(request, "student_panel/grades/grade_list.html", {
        "student":        student,
        "school_class":   school_class,
        "subject_grades": subject_grades,
    })
