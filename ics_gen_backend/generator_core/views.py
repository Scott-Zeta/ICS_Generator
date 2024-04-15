from django.views.generic import TemplateView
from django.http import HttpResponse
from django.utils import timezone
from .models import UploadRecord, DownloadRecord
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Generic View
class IndexView(TemplateView):
    template_name = "generator_core/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        server_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
        recent_upload_record = UploadRecord.objects.order_by('-access_time')[:5]
        recent_download_record = DownloadRecord.objects.order_by('-access_time')[:5]
        context["title"] = "ICS Generator"
        context["server_time"] = server_time
        context["recent_upload_record"] = recent_upload_record
        context["recent_download_record"] = recent_download_record
        return context

@api_view(['POST'])
def upload(request):
    new_record = UploadRecord()
    new_record.save()
    return Response("Upload Entry Point")

@api_view(['GET'])
def download(request):
    new_record = DownloadRecord()
    new_record.save()
    return Response("Download Entry Point")