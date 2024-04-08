from django.urls import path

from . import views

urlpatterns = [
    # ex: /generator_core/
    path("", views.index, name="index"),
    # ex: /generator_core/upload/
    path("upload/", views.upload, name="upload")
]