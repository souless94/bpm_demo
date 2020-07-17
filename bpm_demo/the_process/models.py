from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
import uuid
# Create your models here.

    TYPE_CHOICES = (
        ('Documents and Photos')
        ('Photos')
        ('Supporting Documents')
    )

class Submission(models.Model):
    title = models.CharField(max_length=255)
    state_machine = models.CharField(max_length=255)
    execution_name = models.CharField(max_length=255)
    current_status = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    assignee = models.CharField(max_length=255)
    submit_time = models.DateTimeField('date submitted',default=now)
    objects = models.Manager()

class Findings(models.Model):

    # Section (A) - 1: Observation of Workplace
    SECTIONA_CHOICES = (
        ('Section(A) - 1')
    )
    Section_A = models.CharField(max_length=20000)
    File_A = models.FileField(True)
    Document_Name_A = models.CharField(max_length=100)
    Document_type_A = models.CharField(max_length=20, choices=TYPE_CHOICES)
    Section_of_Group_A = models.CharsField(max_length=20, choices=SECTIONA_CHOICES)
    Description_A = models.CharField(max_length=2000)

    # Section (B) - 1: Observation of Equipment/Machinery/Process
    SECTIONB_CHOICES = (
        ('Section(B) - 1')
    )
    Section_B = models.CharField(max_length=20000)
    File_B = models.FileField(True)
    Document_Name_B = models.CharField(max_length=100)
    Document_type_B = models.CharField(max_length=20, choices=TYPE_CHOICES)
    Section_of_Group_B = models.CharsField(max_length=20, choices=SECTIONB_CHOICES)
    Description_B = models.CharField(max_length=2000)

    # Section (C) - 1: Background
    SECTIONC_CHOICES = (
        ('Section(C) - 1')
    )
    Section_C = models.CharField(max_length=20000)
    File_C = models.FileField(True)
    Document_Name_C = models.CharField(max_length=100)
    Document_type_C = models.CharField(max_length=20, choices=TYPE_CHOICES)
    Section_of_Group_C = models.CharsField(max_length=20, choices=SECTIONC_CHOICES)
    Description_C = models.CharField(max_length=2000)

    # Section (D) - 1: Measures to be taken
    SECTIOND_CHOICES = (
        ('Section(D) - 1')
    )
    Section_D = models.CharField(max_length=20000)
    File_D = models.FileField(True)
    Document_Name_D = models.CharField(max_length=100)
    Document_type_D = models.CharField(max_length=20, choices=TYPE_CHOICES)
    Section_of_Group_D = models.CharsField(max_length=20, choices=SECTIOND_CHOICES)
    Description_D = models.CharField(max_length=2000)

class Risk_Assessment(models.Model):
    RMI_CHOICES = (
        ('Basic')
        ('Good')
        ('Not Applicable')
        ('Not Assessed')
        ('Unsatisfactory')
    )


    RMI = models.CharField(max_length=20, choices=RMI_CHOICES)

    #Add supporting documents
    File = models.FileField(True)
    Document_Name = models.CharField(max_length=100)
    Document_Type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    Questionnaire_Name = models.CharField(max_length=50)
    Question_No = models.IntegerField(True)
    Description = models.CharField(max_length=2000)

class Enforcement(models.Model):
    