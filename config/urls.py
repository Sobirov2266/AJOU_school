from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path("dashboard/", include("apps.dashboard.urls")),
    path("admin-panel/", include("apps.admin_panel.urls")),
    path('logout/', LogoutView.as_view(), name='logout'),

]

# MEDIA (faqat development uchun)
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
