from django.db import models

# Create your models here.

# Ticket Record for Upload entry hit point
class UploadRecord(models.Model):
    acess_time = models.DateTimeField(auto_now_add=True)
    
# Ticket Record for Download entry hit point
class DownloadRecord(models.Model):
    acess_time = models.DateTimeField(auto_now_add=True)