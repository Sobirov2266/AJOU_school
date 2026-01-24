from django.db import models
from django.contrib.auth import get_user_model
from apps.accounts.models import TeacherProfile



User = get_user_model()


class SchoolClass(models.Model):
    name = models.CharField(max_length=50)  # masalan: 9-A, 10-B
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name="classes"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sinf"
        verbose_name_plural = "Sinflar"

    def __str__(self):
        return self.name



# Talaba modeli
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Talaba"
        verbose_name_plural = "Talabalar"

    def __str__(self):
        return self.full_name


#  Sinfga yozilish modeli (Student ↔ Class)
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="enrollments")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "school_class")
        verbose_name = "Sinfga yozilish"
        verbose_name_plural = "Sinfga yozilishlar"

    def __str__(self):
        return f"{self.student} -> {self.school_class}"


# Fan modeli
class Subject(models.Model):
    name = models.CharField(max_length=100)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="subjects")

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"

    def __str__(self):
        return self.name
