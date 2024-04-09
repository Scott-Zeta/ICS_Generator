from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    template = loader.get_template('generator_core/index.html')
    context ={"title": "ICS Generator"}
    return HttpResponse(HttpResponse(template.render(context, request)))

def upload(request):
    template = loader.get_template('generator_core/upload.html')
    context ={"title": "Upload Entry Point"}
    return HttpResponse(HttpResponse(template.render(context, request)))