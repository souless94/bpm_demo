from django.db import models
from django.utils.timezone import now
from jsonfield import JSONField
import uuid
# Create your models here.
class State(models.Model):
    # process inputs later
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    workflow = JSONField()
    assignee = models.CharField(max_length=255,default='Not Assigned')
    submitTime = models.DateTimeField(default=now)
    # to check if state is ready and what else is not ready
    done = models.BooleanField(default=False)
    LeftReady = JSONField(blank=True)

# per screen per form
class CreateInspectionForm(models.Model):
    inspectionCategory = models.CharField(max_length=255)
    inspectionType = models.CharField(max_length=255)
    reference = models.CharField(max_length=255,blank=True)
    referenceNo = models.CharField(max_length=255,blank=True)
    arrivalDate = models.DateField(default=now,blank=True)
    TeamDetails = models.CharField(max_length=255)
    workPlaceNo = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class FindingsForm(models.Model):
    description = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class QuestionaireForm(models.Model):
    # is there any more features? 
    # what features to implement ? feature a, b , c,d
    questions = models.CharField(max_length=255,blank=True)
    responses = models.CharField(max_length=255,blank=True)
    response = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class WarningsForm(models.Model):
    # warnings, stop work order
    enforcementAction = models.CharField(max_length=255)
    law = models.CharField(max_length=255)
    act = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class SWOForm(models.Model):
    # warnings, stop work order
    orderNo = models.CharField(max_length=255)
    proposal = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class ApprovalForm(models.Model):
    clarifications = models.CharField(max_length=255)
    approve = models.BooleanField(default=False)
    officerName = models.CharField(max_length=255)
    remarks = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

