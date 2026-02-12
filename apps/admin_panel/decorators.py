from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.urls import reverse
from apps.accounts.models import User

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.path}")

        if getattr(request.user, "role", None) != User.Role.ADMIN:
            return HttpResponseForbidden("Admin access only")

        return view_func(request, *args, **kwargs)
    return _wrapped
