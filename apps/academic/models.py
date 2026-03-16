from django.db import models
from django.utils import timezone
from ..accounts.models import TeacherProfile, StudentProfile



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


# Dars jadvali model
class Timetable(models.Model):
    WEEKDAY_CHOICES = (
        ("MON", "Dushanba"),
        ("TUE", "Seshanba"),
        ("WED", "Chorshanba"),
        ("THU", "Payshanba"),
        ("FRI", "Juma"),
    )

    PERIOD_TIME_MAP = {
        1: ("08:00", "08:45"),
        2: ("08:50", "09:35"),
        3: ("09:40", "10:25"),
        4: ("10:30", "11:15"),
        5: ("11:20", "12:05"),
        6: ("13:00", "13:45"),
        7: ("13:50", "14:35"),
        8: ("14:40", "15:25"),
        9: ("15:30", "16:15"),
    }

    @classmethod
    def get_period_times(cls, lesson_order):
        return cls.PERIOD_TIME_MAP.get(lesson_order)

    class_subject = models.ForeignKey(
        ClassSubject,
        on_delete=models.CASCADE,
        related_name="timetables",
        verbose_name="Sinf-Fan-O‘qituvchi"
    )
    weekday = models.CharField(
        max_length=3,
        choices=WEEKDAY_CHOICES,
        verbose_name="Hafta kuni"
    )
    lesson_order = models.PositiveIntegerField(
        verbose_name="Dars tartib raqami"
    )
    start_time = models.TimeField(
        verbose_name="Boshlanish vaqti"
    )
    end_time = models.TimeField(
        verbose_name="Tugash vaqti"
    )
    room = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Xona"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faol"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Yaratilgan vaqt"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan vaqt"
    )

    class Meta:
        verbose_name = "Dars jadvali"
        verbose_name_plural = "Dars jadvallari"
        ordering = ["weekday", "lesson_order", "start_time"]
        unique_together = ("class_subject", "weekday", "lesson_order")

    def __str__(self):
        return (
            f"{self.class_subject.school_class} | "
            f"{self.class_subject.subject} | "
            f"{self.get_weekday_display()} | "
            f"{self.lesson_order}-dars"
        )



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


