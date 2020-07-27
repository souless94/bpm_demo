from django.forms import ModelForm
from .models import *


class StepStatusForm(ModelForm):
    class Meta:
        model = StepStatus
        fields = '__all__'


class Update_InspectionForm(ModelForm):
    class Meta:
        model = Update_Inspection
        fields = '__all__'

class Create_InspectionForm(ModelForm):
    class Meta:
        model = Update_Inspection
        fields = '__all__'
        exclude= ['stepStatus',]


class FindingsForm(ModelForm):
    class Meta:
        model = Findings
        fields = '__all__'
        exclude= ['finished',]


class Risk_AssessmentForm(ModelForm):
    class Meta:
        model = Risk_Assessment
        fields = '__all__'


class WarningsForm(ModelForm):
    class Meta:
        model = Warnings
        fields = '__all__'


class SWOForm(ModelForm):
    class Meta:
        model = SWO
        fields = '__all__'


class ApprovalActionForm(ModelForm):
    class Meta:
        model = ApprovalAction
        fields = '__all__'


class ApproveOfficerForm(ModelForm):
    class Meta:
        model = ApproveOfficer
        fields = '__all__'
