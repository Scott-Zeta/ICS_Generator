from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
import datetime

# Create your views here.
def index(request):
    template = loader.get_template('generator_core/index.html')
    server_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
    context ={"title": "ICS Generator", "server_time": server_time}
    return HttpResponse(HttpResponse(template.render(context, request)))

def upload(request):
    template = loader.get_template('generator_core/upload.html')
    context ={"title": "Upload Entry Point"}
    return HttpResponse(HttpResponse(template.render(context, request)))