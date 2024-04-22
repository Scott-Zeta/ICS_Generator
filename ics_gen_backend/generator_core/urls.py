from django.urls import path
from .views import IndexView, UploadView
from . import views

app_name = "generator_core"
urlpatterns = [
    # ex: /generator_core/
    path("", IndexView.as_view(), name="index"),
    # ex: /generator_core/upload/
    path("upload/", UploadView.as_view()),
    # ex: /generator_core/download/
    path("download/", views.download)
]