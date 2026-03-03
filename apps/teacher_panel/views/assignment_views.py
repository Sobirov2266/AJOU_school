from django.http import HttpResponse
from ..decorators import teacher_required


@teacher_required
def assignments_list_view(request):
    return HttpResponse("Assignments page")