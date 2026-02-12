from django.db import models
from django.utils import timezone
from apps.accounts.models import TeacherProfile, StudentProfile



# =========================
# SINFLAR
# =========================
class SchoolClass(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Sinf nomi"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Sinf"
        verbose_name_plural = "Sinflar"
        ordering = ["name"]

    def __str__(self):
        return self.name





# =========================
# FANLAR
# =========================
class Subject(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Fan nomi"
    )
    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Fan kodi"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"





# =========================
# SINF ↔ FAN ↔ O‘QITUVCHI
# =========================
class ClassSubject(models.Model):
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="class_subjects",
        verbose_name="Sinf"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="class_subjects",
        verbose_name="Fan"
    )
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="class_subjects",
        verbose_name="O‘qituvchi"
    )
    weekly_hours = models.PositiveIntegerField(
        default=0,
        verbose_name="Haftalik soat"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Sinf fani"
        verbose_name_plural = "Sinf fanlari"
        unique_together = ("school_class", "subject")
        ordering = ["school_class", "subject"]

    def __str__(self):
        return f"{self.school_class} → {self.subject} ({self.teacher})"






# =========================
# O‘QUVCHI ↔ SINF
# =========================
class Enrollment(models.Model):
    student = models.OneToOneField(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="enrollment"
    )
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    enrolled_at = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "O‘quvchini sinfga biriktirish"
        verbose_name_plural = "O‘quvchilar sinflari"

    def __str__(self):
        return f"{self.student} → {self.school_class}"


