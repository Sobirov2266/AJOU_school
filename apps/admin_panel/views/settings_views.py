from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect, render

from apps.admin_panel.decorators import admin_required
from apps.admin_panel.forms import AdminPasswordChangeForm, AdminProfileForm


@admin_required
def admin_settings(request):
    """Admin Settings page.

    - Only logged-in admins can access (admin_required).
    - Admin can update own profile fields + optional photo.
    - Admin can change password using Django's built-in PasswordChangeForm.
    - update_session_auth_hash keeps the admin logged in after password change.
    """

    user = request.user

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "profile":
            profile_form = AdminProfileForm(
                request.POST,
                request.FILES,
                instance=user,
            )
            password_form = AdminPasswordChangeForm(user=user)

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profil ma’lumotlari yangilandi")
                return redirect("admin_panel:admin_settings")

        elif action == "password":
            profile_form = AdminProfileForm(instance=user)
            password_form = AdminPasswordChangeForm(user=user, data=request.POST)

            if password_form.is_valid():
                updated_user = password_form.save()

                # IMPORTANT: keep user logged in after password change
                update_session_auth_hash(request, updated_user)

                messages.success(request, "Parol muvaffaqiyatli yangilandi")
                return redirect("admin_panel:admin_settings")

        else:
            profile_form = AdminProfileForm(instance=user)
            password_form = AdminPasswordChangeForm(user=user)
            messages.error(request, "Noto‘g‘ri so‘rov")

    else:
        profile_form = AdminProfileForm(instance=user)
        password_form = AdminPasswordChangeForm(user=user)

    return render(
        request,
        "admin_panel/settings.html",
        {
            "profile_form": profile_form,
            "password_form": password_form,
        },
    )
