from django.urls import path

from .password_views import StudentPasswordChangeView
from .views import CustomLoginView


app_name = "accounts"

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('password-change/', StudentPasswordChangeView.as_view(), name='password_change'),
]

