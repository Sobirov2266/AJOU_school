from django.contrib import admin
from .models import SchoolClass, Subject, Enrollment, ClassSubject


admin.site.register(SchoolClass)
admin.site.register(Subject)
admin.site.register(ClassSubject)
admin.site.register(Enrollment)