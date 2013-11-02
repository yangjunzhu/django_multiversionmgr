from django.http import HttpResponse
from django.shortcuts import render_to_response

def hello(request):
    return HttpResponse("Hello, django!")

def createversion(request):
    from createversionform import *
    form = CreateVersionForm()
    return render_to_response('createversion.html', {'form': form})
