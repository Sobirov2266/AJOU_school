from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from ...assignments.forms import AssignmentCreateForm
from ...assignments.models import Assignment

from ..decorators import teacher_required


@teacher_required
def assignment_list_view(request):
    teacher_profile = getattr(request.user, "teacher_profile", None)

    assignments = (
        Assignment.objects
        .select_related(
            "class_subject",
            "class_subject__school_class",
            "class_subject__subject",
            "class_subject__teacher",
        )
        .filter(class_subject__teacher=teacher_profile)
        .order_by("-created_at")
    )

    context = {
        "assignments": assignments,
        "published_count": assignments.filter(is_published=True).count(),
        "draft_count": assignments.filter(is_published=False).count(),
        "total_count": assignments.count(),
    }
    return render(request, "teacher_panel/assignments/assignment_list.html", context)


@teacher_required
def assignment_create_view(request):
    teacher_profile = getattr(request.user, "teacher_profile", None)

    if request.method == "POST":
        form = AssignmentCreateForm(
            request.POST,
            request.FILES,
            teacher_profile=teacher_profile,
        )
        if form.is_valid():
            assignment = form.save()
            messages.success(request, "Topshiriq muvaffaqiyatli yaratildi.")
            return redirect("teacher_panel:assignment_detail", pk=assignment.pk)
    else:
        form = AssignmentCreateForm(teacher_profile=teacher_profile)

    context = {
        "form": form,
        "page_title": "Topshiriq yaratish",
    }
    return render(request, "teacher_panel/assignments/assignment_form.html", context)


@teacher_required
def assignment_detail_view(request, pk):
    teacher_profile = getattr(request.user, "teacher_profile", None)

    assignment = get_object_or_404(
        Assignment.objects.select_related(
            "class_subject",
            "class_subject__school_class",
            "class_subject__subject",
            "class_subject__teacher",
        ),
        pk=pk,
        class_subject__teacher=teacher_profile,
    )

    submissions = (
        assignment.submissions
        .select_related("student", "student__user")
        .order_by("-submitted_at")
    )

    context = {
        "assignment": assignment,
        "submissions": submissions,
        "submission_count": submissions.count(),
        "reviewed_count": submissions.filter(status="reviewed").count(),
    }
    return render(request, "teacher_panel/assignments/assignment_detail.html", context)