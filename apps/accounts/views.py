from django.contrib.auth.views import LoginView
from .models import User


class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser:
            return '/admin/'

        if user.role == User.Role.TEACHER:
            return '/dashboard/teacher/'

        if user.role == User.Role.STUDENT:
            return '/dashboard/student/'

        return '/'


class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser:
            return '/admin/'

        if user.role == User.Role.ADMIN:
            return '/admin-panel/dashboard/'

        if user.role == User.Role.TEACHER:
            return '/dashboard/teacher/'

        if user.role == User.Role.STUDENT:
            return '/dashboard/student/'

        return '/'