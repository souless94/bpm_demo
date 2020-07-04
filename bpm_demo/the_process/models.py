from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
import uuid
# Create your models here.

CHOICES = [
    ('start','start'),
    ('verify','verify'),
    ('reassign','reassign'),
    ('approve','approve')
]

class Role(models.Model):
    name = models.CharField(primary_key=True,max_length=255)
    objects = models.Manager()

class Task(models.Model):
    submission_id = models.CharField('submission_id', primary_key=True,max_length=255,default=str(uuid.uuid4()))
    description = models.TextField('description')
    status = models.CharField(max_length=255,choices=CHOICES,blank=True)
    assignee = models.ForeignKey(Role,on_delete=models.CASCADE)
    diagram = models.TextField('diagram',blank=True)
    username = models.CharField(max_length=255,default="No User")
    objects = models.Manager()

class state(models.Model):
    submission = models.ForeignKey(Task,on_delete=models.CASCADE)
    execution_arn = models.CharField(max_length=255)
    amount = models.FloatField('amount',blank=True)
    status = models.CharField(max_length=255,choices=CHOICES)
    the_file = models.FileField(upload_to='file_uploads',blank=True)
    submit_time = models.DateTimeField('date submitted',default=now)
    comment = models.TextField('comment',blank=True)
    objects = models.Manager()
