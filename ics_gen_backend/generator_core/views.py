from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from .models import UploadRecord, DownloadRecord

# Create your views here.
def index(request):
    template = loader.get_template('generator_core/index.html')
    server_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
    recent_upload_record = UploadRecord.objects.order_by('-access_time')[:5]
    recent_download_record = DownloadRecord.objects.order_by('-access_time')[:5]
    context ={"title": "ICS Generator", "server_time": server_time, 
              "recent_upload_record": recent_upload_record,
              "recent_download_record": recent_download_record}
    return HttpResponse(template.render(context, request))

def upload(request):
    context ={}
    return HttpResponse("Upload Entry Point")