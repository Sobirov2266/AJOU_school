from django import forms
from django.utils import timezone

from .models import Assignment


class AssignmentCreateForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = Assignment
        fields = [
            "class_subject",
            "title",
            "description",
            "due_date",
            "max_score",
            "attachment",
            "is_published",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Masalan: 2-mavzu bo‘yicha uyga vazifa"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Topshiriq tafsilotlarini yozing...",
                }
            ),
            "class_subject": forms.Select(attrs={"class": "form-control"}),
            "max_score": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "placeholder": "100"}
            ),
            "attachment": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        teacher_profile = kwargs.pop("teacher_profile", None)
        super().__init__(*args, **kwargs)

        self.fields["due_date"].widget.attrs["class"] = "form-control"

        if teacher_profile is not None:
            self.fields["class_subject"].queryset = (
                self.fields["class_subject"]
                .queryset
                .filter(
                    teacher=teacher_profile,
                    is_active=True,
                    subject__is_active=True,
                    school_class__is_active=True,
                )
                .select_related("school_class", "subject")
                .order_by("school_class__name", "subject__name")
            )

    def clean_due_date(self):
        due_date = self.cleaned_data["due_date"]
        if due_date <= timezone.now():
            raise forms.ValidationError("Deadline hozirgi vaqtdan keyin bo‘lishi kerak.")
        return due_date