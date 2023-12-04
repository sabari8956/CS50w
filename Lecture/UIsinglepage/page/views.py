from django.shortcuts import render
from django.http import HttpResponse, Http404
# Create your views here.


def index(req):
    return render(req, "page/index.html")


texts = ["Text 1", "Text 2", "Text 3"]

def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(texts[num - 1])
    else:
        raise Http404("No such section")