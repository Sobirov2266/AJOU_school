from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from ..accounts.models import User


def student_required(view_func):
    """
    Faqat STUDENT rolidagi foydalanuvchilarga ruxsat beradi.
    Login qilinmagan yoki boshqa rol bo'lsa — login sahifasiga yo'naltiradi.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect("accounts:login")

        if getattr(user, "role", None) != User.Role.STUDENT:
            messages.error(request, "Sizda student panelga kirish huquqi yo'q.")
            return redirect("accounts:login")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
