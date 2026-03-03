from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from ..accounts.models import User


def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        # Login qilmagan bo'lsa
        if not user.is_authenticated:
            return redirect("accounts:login")

        # Superuser/admin teacher panelga kirmasin (xohlasangiz ruxsat berish ham mumkin)
        if getattr(user, "role", None) != User.Role.TEACHER:
            messages.error(request, "Sizda teacher panelga kirish huquqi yo‘q.")
            return redirect("accounts:login")  # yoki "/" yoki admin dashboard

        return view_func(request, *args, **kwargs)

    return _wrapped_view