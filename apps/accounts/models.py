from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


# Teacher malumotlari
class TeacherProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Erkak'),
        ('female', 'Ayol'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )

    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)

    birth_year = models.PositiveIntegerField(null=True, blank=True)

    passport_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    jshshr = models.CharField(max_length=14, unique=True, null=True, blank=True)

    subject = models.ForeignKey(
        'academic.Subject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


# student ma'lumotlari
class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    # Asosiy ma’lumotlar
    first_name = models.CharField("Ismi", max_length=100)
    last_name = models.CharField("Familiyasi", max_length=100)

    birth_date = models.DateField(
        "Tug‘ilgan sana",
        null=True,
        blank=True
    )



    # Hujjatlar
    passport_id = models.CharField(
        "Passport yoki guvohnoma ID",
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    # Ota-ona aloqa
    parent_phone = models.CharField(
        "Ota-ona telefoni",
        max_length=20
    )

    # Profil rasmi
    avatar = models.ImageField(
        upload_to="students/avatars/",
        null=True,
        blank=True
    )

    # Status (user.is_active bilan bog‘liq)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

