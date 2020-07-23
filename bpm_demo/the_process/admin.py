from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.StepStatus)
admin.site.register(models.Update_Inspection)
admin.site.register(models.SWO)
admin.site.register(models.Warnings)
admin.site.register(models.ApprovalAction)