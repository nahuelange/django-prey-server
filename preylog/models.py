from django.db import models

class API_User(models.Model):
    username = models.CharField(max_length=255)

class Device(models.Model):
    user       = models.ForeignKey(API_User, related_name="devices")
    key        = models.CharField(max_length=255)
    lost       = models.BooleanField(default=False)
    title      = models.CharField(max_length=255)
    os_version = models.CharField(max_length=255)
    os         = models.CharField(max_length=255)
    genre      = models.CharField(max_length=255)

class Report(models.Model):
    device     = models.ForeignKey(Device, related_name="reports")
    data       = models.TextField()

class ReportFile(models.Model):
    report     = models.ForeignKey(Report, related_name="files")
    filename   = models.FileField(upload_to = "files")