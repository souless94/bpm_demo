from django.db import models
from django.utils.timezone import now
from jsonfield import JSONField
import uuid
# Create your models here.

class ProcessForm(models.Model):
    # process inputs later
    name = models.CharField(max_length=255)
    comments = models.TextField()
    fileUpload = models.FileField( upload_to='file_uploads',blank=True)

class State(models.Model):
    # process inputs later
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    workflow = JSONField()
    assignee = models.CharField(max_length=255,default='Not Assigned')
    submitTime = models.DateTimeField(default=now)