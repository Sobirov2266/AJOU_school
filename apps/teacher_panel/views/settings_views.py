from django.http import HttpResponse
from ..decorators import teacher_required

@teacher_required
def settings_view(request):
    return HttpResponse("settings page")