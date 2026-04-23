from django.contrib import admin

from .models import Assignment, AssignmentSubmission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "class_subject",
        "due_date",
        "max_score",
        "is_published",
        "created_at",
    )
    list_filter = (
        "is_published",
        "class_subject__subject",
        "class_subject__school_class",
        "created_at",
    )
    search_fields = (
        "title",
        "description",
        "class_subject__subject__name",
        "class_subject__school_class__name",
        "class_subject__teacher__user__username",
    )


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "assignment",
        "student",
        "status",
        "score",
        "submitted_at",
        "reviewed_at",
    )
    list_filter = (
        "status",
        "submitted_at",
        "reviewed_at",
        "assignment__class_subject__subject",
        "assignment__class_subject__school_class",
    )
    search_fields = (
        "assignment__title",
        "student__user__username",
        "student__first_name",
        "student__last_name",
        "feedback",
    )