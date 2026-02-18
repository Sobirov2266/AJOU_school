from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import RegexValidator
from django.db import transaction

from apps.academic.models import Enrollment, SchoolClass, Subject
from apps.accounts.models import StudentProfile

User = get_user_model()


class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "profile_photo",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].required = True
        self.fields["email"].required = False
        self.fields["profile_photo"].required = False


class AdminPasswordChangeForm(PasswordChangeForm):
    pass


class StudentCreateForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    birth_date = forms.DateField(required=False)

    passport_id = forms.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{2}\d{7}$",
                message="Passport formati: 2 ta katta harf + 7 ta raqam (masalan: AB1234567).",
            )
        ],
    )
    parent_phone = forms.CharField(max_length=13)
    avatar = forms.ImageField(required=False)
    school_class = forms.ModelChoiceField(queryset=SchoolClass.objects.all())

    def clean_first_name(self):
        first_name = (self.cleaned_data.get("first_name") or "").strip()
        if not first_name:
            return first_name

        # Only letters (no digits/symbols)
        # \W also excludes underscore, keep unicode letters only
        import re

        if not re.match(r"^[^\W\d_]+$", first_name, flags=re.UNICODE):
            raise forms.ValidationError("Ism faqat harflardan iborat bo‘lishi kerak.")
        return first_name

    def clean_passport_id(self):
        passport_id = (self.cleaned_data.get("passport_id") or "").strip()
        if not passport_id:
            raise forms.ValidationError("Passport/ID majburiy.")
        return passport_id.upper()

    def clean_parent_phone(self):
        phone = (self.cleaned_data.get("parent_phone") or "").strip()

        if not phone:
            raise forms.ValidationError("Telefon raqam majburiy.")

        if not phone.startswith("+"):
            phone = "+" + phone

        digits = phone[1:]
        if not digits.isdigit():
            raise forms.ValidationError("Telefon raqamda '+' dan keyin faqat raqam bo‘lishi kerak.")

        if len(digits) != 12:
            raise forms.ValidationError("Telefon raqam '+' dan keyin 12 ta raqamdan iborat bo‘lishi kerak.")

        return "+" + digits

    def _normalize_for_username(self, text: str) -> str:
        """Normalize name parts for username generation.

        - Lowercase
        - Remove spaces and most special characters
        - Keep only letters/digits
        """

        import re
        import unicodedata

        text = unicodedata.normalize("NFKD", text or "")
        text = text.lower().strip()
        text = re.sub(r"\s+", "", text)
        # Keep unicode letters/digits only
        text = re.sub(r"[^\w\d]+", "", text, flags=re.UNICODE)
        # Remove underscores (\w includes underscore)
        text = text.replace("_", "")
        return text

    def _generate_unique_username(self, first_name: str, last_name: str) -> str:
        """Generate username in the format: l.firstname (with numeric suffix if needed)."""

        fn = self._normalize_for_username(first_name)
        ln = self._normalize_for_username(last_name)

        base_letter = ln[:1] if ln else "u"
        base_first = fn or "student"
        base = f"{base_letter}.{base_first}"

        candidate = base
        suffix = 0
        while User.objects.filter(username=candidate).exists():
            suffix += 1
            candidate = f"{base}{suffix}"
        return candidate

    def clean(self):
        cleaned = super().clean()

        # Duplicate prevention (backend): passport_id must be unique.
        passport_id = cleaned.get("passport_id")
        if passport_id and StudentProfile.objects.filter(passport_id=passport_id).exists():
            self.add_error(
                "passport_id",
                "Siz yaratgan talaba oldin yaratilgan, oldin tekshirib qayta ma'lumotlarni kiriting.",
            )

        # Auto-generate login for preview/redisplay.
        first_name = cleaned.get("first_name")
        last_name = cleaned.get("last_name")
        if first_name and last_name:
            cleaned["generated_username"] = self._generate_unique_username(first_name, last_name)

        return cleaned

    def save(self, request):
        """Create User + StudentProfile + Enrollment.

        IMPORTANT: use transaction.atomic to avoid partial creation.
        """

        with transaction.atomic():
            # Login and password are generated automatically:
            # - username: l.firstname (+ numeric suffix if needed)
            # - initial password: passport_id
            username = self._generate_unique_username(
                self.cleaned_data["first_name"],
                self.cleaned_data["last_name"],
            )
            initial_password = self.cleaned_data["passport_id"]

            user = User.objects.create_user(
                username=username,
                password=initial_password,
                role="STUDENT",
                is_active=True,
            )

            student = StudentProfile.objects.create(
                user=user,
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
                birth_date=self.cleaned_data.get("birth_date"),
                passport_id=self.cleaned_data.get("passport_id"),
                parent_phone=self.cleaned_data["parent_phone"],
                avatar=self.cleaned_data.get("avatar"),
            )

            Enrollment.objects.create(
                student=student,
                school_class=self.cleaned_data["school_class"],
                is_active=True,
            )

        return student


class ClassNameForm(forms.Form):
    name = forms.CharField(max_length=20)

    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = instance

    def clean_name(self):
        import re

        raw = (self.cleaned_data.get("name") or "").strip()
        if not raw:
            raise forms.ValidationError("Sinf nomi majburiy.")

        # Normalize: digits + '-' + letter
        raw = raw.replace(" ", "")
        m = re.match(r"^(\d+)-?([A-Za-z])$", raw)
        if not m:
            raise forms.ValidationError("Sinf nomi formati: raqam-dash-harf (masalan: 7-A).")

        number, letter = m.group(1), m.group(2).upper()
        normalized = f"{number}-{letter}"

        # Duplicate prevention (backend): do not allow same normalized class name.
        qs = SchoolClass.objects.filter(name=normalized)
        if self.instance and getattr(self.instance, "pk", None):
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "Siz bu sinfni oldin yaratgansiz. Iltimos tekshirib, boshqa sinf yarating."
            )

        return normalized


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "code", "is_active"]

    def clean_code(self):
        code = (self.cleaned_data.get("code") or "").strip()
        if not code:
            raise forms.ValidationError("Kod majburiy.")
        return code.upper()

    def clean(self):
        cleaned = super().clean()

        # Duplicate prevention (backend): subject code must be unique.
        code = cleaned.get("code")

        qs = Subject.objects.all()
        if self.instance and getattr(self.instance, "pk", None):
            qs = qs.exclude(pk=self.instance.pk)

        if code and qs.filter(code__iexact=code).exists():
            self.add_error("code", "Bu fan kodi allaqachon mavjud.")

        return cleaned
