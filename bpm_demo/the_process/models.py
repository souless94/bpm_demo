from django.db import models
from django.utils.timezone import now
from jsonfield import JSONField
import uuid
# Create your models here.

class ProcessForm(models.Model):
    # process inputs later
    name = models.CharField(max_length=255)
    inputs = JSONField()
    fileUpload = models.FileField(blank=True, upload_to='file_uploads')

class State(models.Model):
    # process inputs later
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    workflow = JSONField()
    submitTime = models.DateTimeField(default=now)