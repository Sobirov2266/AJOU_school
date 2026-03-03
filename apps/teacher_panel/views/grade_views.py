from django.http import HttpResponse
from ..decorators import teacher_required

@teacher_required
def grade_enter_view(request):
    return HttpResponse("garde page")