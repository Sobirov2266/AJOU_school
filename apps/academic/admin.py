from django.contrib import admin
from .models import SchoolClass, Subject, Student, Enrollment

admin.site.register(SchoolClass)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Enrollment)
