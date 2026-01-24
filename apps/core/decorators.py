from django.http import HttpResponseForbidden
from functools import wraps


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required")

            user_role = str(request.user.role).upper()  # 🔥 MUHIM

            allowed = [str(role).upper() for role in allowed_roles]

            if user_role not in allowed:
                return HttpResponseForbidden(
                    f"You do not have permission. Your role: {user_role}, Allowed: {allowed}"
                )

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator
