from django.http import HttpResponse
from ..decorators import teacher_required

@teacher_required
def test_view(request):
    return HttpResponse("test page")