from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from apps.academic.models import SchoolClass
from apps.admin_panel.decorators import admin_required

@admin_required
def class_list(request):
    q = request.GET.get("q", "").strip()
    classes = SchoolClass.objects.all().order_by("name")

    if q:
        classes = classes.filter(Q(name__icontains=q))

    return render(request, "admin_panel/classes/class_list.html", {
        "classes": classes,
        "class_count": classes.count(),
        "q": q
    })


@admin_required
def class_create(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        if name:
            SchoolClass.objects.create(name=name)
    return redirect("admin_panel:class_list")


@admin_required
def class_update(request):
    if request.method == "POST":
        class_id = request.POST.get("class_id")
        school_class = get_object_or_404(SchoolClass, id=class_id)

        school_class.name = (request.POST.get("name") or "").strip()
        school_class.is_active = (request.POST.get("is_active") == "1")
        school_class.save()
    return redirect("admin_panel:class_list")


@admin_required
def class_delete(request, id):
    school_class = get_object_or_404(SchoolClass, id=id)
    school_class.delete()
    return redirect("admin_panel:class_list")


@admin_required
def class_toggle_status(request, id):
    school_class = get_object_or_404(SchoolClass, id=id)
    school_class.is_active = not school_class.is_active
    school_class.save(update_fields=["is_active"])
    return redirect("admin_panel:class_list")
