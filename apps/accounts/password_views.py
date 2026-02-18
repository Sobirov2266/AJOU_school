from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from .models import User


class StudentPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:password_change")

    def get_success_url(self):
        user = self.request.user
        if getattr(user, "role", None) == User.Role.ADMIN:
            return "/admin-panel/dashboard/"
        if getattr(user, "role", None) == User.Role.TEACHER:
            return "/dashboard/teacher/"
        if getattr(user, "role", None) == User.Role.STUDENT:
            return "/dashboard/student/"
        return "/"

    def form_valid(self, form):
        response = super().form_valid(form)

        # Keep user logged in after changing password
        update_session_auth_hash(self.request, self.request.user)

        # Disable first-login password-change requirement
        user = self.request.user
        if hasattr(user, "must_change_password") and user.must_change_password:
            user.must_change_password = False
            user.save(update_fields=["must_change_password"])

        messages.success(self.request, "Parol muvaffaqiyatli yangilandi")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Parolni yangilashda xatolik bor. Iltimos tekshirib qayta urinib ko‘ring.")
        return super().form_invalid(form)
