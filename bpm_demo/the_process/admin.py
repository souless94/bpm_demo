from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from . import models

class Update_InspectionAdmin(admin.ModelAdmin):
    list_display = ('stepStatus',)
    search_fields = ['stepStatus__id',]

class FindingsAdmin(admin.ModelAdmin):
    list_display = ('stepStatus',)
    search_fields = ['stepStatus__id',]

class WarningsAdmin(admin.ModelAdmin):
    list_display = ('stepStatus',)
    search_fields = ['stepStatus__id',]

class QuestionaireAdmin(admin.ModelAdmin):
    list_display = ('stepStatus',)
    search_fields = ['stepStatus__id',]

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('stepStatus','question_text',)
    search_fields = ['stepStatus__id','question_text',]

class QuestionAdderAdmin(admin.ModelAdmin):
    list_display = ('question_text',)
    search_fields = ['question_text',]

class SWOAdmin(admin.ModelAdmin):
    list_display = ('stepStatus',)
    search_fields = ['stepStatus__id',]

class ApprovalActionAdmin(admin.ModelAdmin):
    list_display = ('stepStatus',)
    search_fields = ['stepStatus__id',]

class ApproveOfficerAdmin(admin.ModelAdmin):
    list_display = ('stepStatus',)
    search_fields = ['stepStatus__id',]

# Register your models here.
admin.site.register(models.StepStatus,SimpleHistoryAdmin)
admin.site.register(models.Update_Inspection,Update_InspectionAdmin)
admin.site.register(models.Findings,FindingsAdmin)
admin.site.register(models.Questionaire,QuestionaireAdmin)
admin.site.register(models.QuestionAdder,QuestionAdderAdmin)
admin.site.register(models.Question,QuestionAdmin)
admin.site.register(models.Warnings,WarningsAdmin)
admin.site.register(models.SWO,SWOAdmin)
admin.site.register(models.ApprovalAction,ApprovalActionAdmin)
admin.site.register(models.ApproveOfficer,ApproveOfficerAdmin)