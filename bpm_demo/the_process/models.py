from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
import uuid
# Create your models here.


class Submission(models.Model):
    title = models.CharField(max_length=255)
    state_machine = models.CharField(max_length=255)
    execution_name = models.CharField(max_length=255)
    current_status = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    assignee = models.CharField(max_length=255)
    submit_time = models.DateTimeField('date submitted',default=now)
    objects = models.Manager()
