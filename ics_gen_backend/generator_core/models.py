from django.db import models

# Create your models here.

# Ticket Record for Upload entry hit point
class UploadRecord(models.Model):
    access_time = models.DateTimeField(auto_now_add=True)
    
    def formatted_time(self):
        return self.access_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
    
# Ticket Record for Download entry hit point
class DownloadRecord(models.Model):
    access_time = models.DateTimeField(auto_now_add=True)
    
    def formatted_time(self):
        return self.access_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]