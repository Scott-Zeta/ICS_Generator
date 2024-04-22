from django.views.generic import TemplateView
from django.utils import timezone
from .models import UploadRecord, DownloadRecord
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PostSerializer
from rest_framework.parsers import MultiPartParser, FormParser

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


class UploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        try:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                new_record = UploadRecord()
                new_record.save()
                text_wait_for_process = serializer.validated_data.get('text','')
                image_wait_for_process = serializer.validated_data.get('image','')
                # more process implementation here
                return Response({"Message":"Valid Input"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Message":f"Internal Server Error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def download(request):
    new_record = DownloadRecord()
    new_record.save()
    return Response("Download Entry Point")