from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
import uuid
# Create your models here.

TYPE_CHOICES = (
    ('Documents and Photos', 'Documents and Photos'),
    ('Photos', 'Photos'),
    ('Supporting Documents', 'Supporting Documents')
)


class StepStatus(models.Model):
    title = models.CharField(max_length=255)
    state_machine = models.CharField(max_length=255)
    execution_arn = models.CharField(max_length=255)
    main = models.CharField(max_length=255)
    current_status = models.CharField(max_length=255)
    assignee = models.CharField(max_length=255)
    submit_time = models.DateTimeField('date submitted', default=now)
    objects = models.Manager()


class Update_Inspection(models.Model):
    REFERENCE_CHOICES = (
        ('Case Management & Investigation', 'Case Management & Investigation'),
        ('Feedback and Appeal', 'Feedback and Appeal'),
        ('Incident Reporting', 'Incident Reporting'),
        ('Inspection & Engagement', 'Inspection & Engagement'),
        ('Monitoring and Surveillance', 'Monitoring and Surveillance')
    )
    Inspection_Category = models.CharField(max_length=100)
    Inspection_Type = models.CharField(max_length=100)
    Reference = models.CharField(max_length=100, choices=REFERENCE_CHOICES)
    Reference_No = models.CharField(max_length=100)
    Arrival_Date = models.DateTimeField(default=now)
    Arrival_Time = models.DateTimeField(default=now)
    Workplace_No = models.CharField(max_length=100)
    objects = models.Manager()


class Findings(models.Model):

    # Section (A) - 1: Observation of Workplace
    SECTIONA_CHOICES = (
        ('Section(A) - 1', 'Section(A) - 1')
    )
    Section_A = models.CharField(max_length=255)
    Document_Name = models.CharField(max_length=255)
    Document_type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    Section_of_Group = models.CharsField(
        max_length=20, choices=SECTIONA_CHOICES)
    Description_A = models.CharField(max_length=255)
    objects = models.Manager()


class Risk_Assessment(models.Model):
    RMI_CHOICES = (
        ('Basic', 'Basic'),
        ('Good', 'Good'),
        ('Not Applicable', 'Not Applicable'),
        ('Not Assessed', 'Not Assessed'),
        ('Unsatisfactory', 'Unsatisfactory')
    )
    Response = models.CharField(max_length=20, choices=RMI_CHOICES)
    Question = models.CharField(max_length=255)
    Description = models.CharField(max_length=255)
    objects = models.Manager()


class Warnings(models.Model):
    Warning_CHOICES = (
        ('Composition Fine', 'Composition Fine'),
        ('Warning', 'Warning'),
        ('Notice', 'Notice')
    )
    proposed_enforcement_action = models.CharField(
        max_length=20, choices=Warning_CHOICES)
    Act = models.CharField(max_length=255)
    Law = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    objects = models.Manager()


class SWO(models.Model):
    justification = models.CharField(max_length=255)
    offenderDetails = models.CharField(max_length=255)
    objects = models.Manager()


class ApprovalAction(models.Model):
    Decision_CHOICES = (
        ('Support', 'Support'),
        ('Reject', 'Reject')
    )
    decision = models.CharField(max_length=255, choices=Decision_CHOICES)
    remarks = models.CharField(max_length=255)
    objects = models.Manager()


class ApproveOfficer(models.Model):
    Decision_CHOICES = (
        ('Approve', 'Approve'),
        ('Reassign', 'Reassign')
    )
    decision = models.CharField(max_length=255, choices=Decision_CHOICES)
    objects = models.Manager()
