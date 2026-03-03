from django.http import HttpResponse
from django.contrib.auth.decorators import login_required



@login_required
def teacher_dashboard(request):
    return HttpResponse("assalomu alaykum viz vanihoyat uddaladik teacherjon!!")