from django.http import HttpResponse
from ..decorators import teacher_required

@teacher_required
def attendance_mark_view(request):
    return HttpResponse("Attendance page")