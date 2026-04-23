from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from ..accounts.models import StudentProfile
from ..academic.models import ClassSubject


def assignment_attachment_upload_path(instance, filename):
    subject_name = instance.class_subject.subject.name.replace(" ", "_")
    class_name = instance.class_subject.school_class.name.replace(" ", "_")
    return f"assignments/teacher_files/{class_name}/{subject_name}/{filename}"


def submission_attachment_upload_path(instance, filename):
    assignment_id = instance.assignment_id or "unknown"
    student_id = instance.student_id or "unknown"
    return f"assignments/student_submissions/assignment_{assignment_id}/student_{student_id}/{filename}"


class Assignment(models.Model):
    class_subject = models.ForeignKey(
        ClassSubject,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    max_score = models.PositiveIntegerField(default=100)
    attachment = models.FileField(
        upload_to=assignment_attachment_upload_path,
        blank=True,
        null=True,
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"

    def __str__(self):
        return f"{self.title} - {self.class_subject}"

    def clean(self):
        errors = {}

        if self.max_score <= 0:
            errors["max_score"] = "Max score 0 dan katta bo‘lishi kerak."

        if self.due_date <= timezone.now():
            errors["due_date"] = "Deadline hozirgi vaqtdan keyin bo‘lishi kerak."

        if not self.class_subject.is_active:
            errors["class_subject"] = "Faol bo‘lmagan class subject uchun assignment yaratib bo‘lmaydi."

        if errors:
            raise ValidationError(errors)

    @property
    def is_overdue(self):
        return timezone.now() > self.due_date

    @property
    def school_class(self):
        return self.class_subject.school_class

    @property
    def subject(self):
        return self.class_subject.subject

    @property
    def teacher(self):
        return self.class_subject.teacher


class AssignmentSubmission(models.Model):
    STATUS_SUBMITTED = "submitted"
    STATUS_REVIEWED = "reviewed"
    STATUS_LATE = "late"

    STATUS_CHOICES = [
        (STATUS_SUBMITTED, "Submitted"),
        (STATUS_REVIEWED, "Reviewed"),
        (STATUS_LATE, "Late"),
    ]

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="assignment_submissions",
    )
    answer_text = models.TextField(blank=True)
    attachment = models.FileField(
        upload_to=submission_attachment_upload_path,
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_SUBMITTED,
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Assignment Submission"
        verbose_name_plural = "Assignment Submissions"
        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "student"],
                name="unique_assignment_submission_per_student",
            )
        ]

    def __str__(self):
        return f"{self.student} -> {self.assignment.title}"

    def clean(self):
        errors = {}

        if not self.answer_text and not self.attachment:
            errors["answer_text"] = "Javob matni yoki fayl bo‘lishi kerak."

        if self.score is not None:
            if self.score < 0:
                errors["score"] = "Baho manfiy bo‘lishi mumkin emas."

            if self.assignment_id and self.score > self.assignment.max_score:
                errors["score"] = f"Baho {self.assignment.max_score} dan katta bo‘lishi mumkin emas."

        if errors:
            raise ValidationError(errors)

    @property
    def is_reviewed(self):
        return self.status == self.STATUS_REVIEWED

    @property
    def is_late(self):
        return self.status == self.STATUS_LATE