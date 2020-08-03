from django.forms import ModelForm, modelformset_factory,ChoiceField, RadioSelect
from .models import *
from django.utils.safestring import mark_safe

class HorizontalRadioRenderer(RadioSelect):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        exclude = ['stepStatus','questionAdder']
    answer = ChoiceField(choices=Question.RMI_CHOICES,
                 initial=0,
                 widget=RadioSelect(),
                                 )

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


class QuestionaireForm(ModelForm):
    class Meta:
        model = Questionaire
        fields = '__all__'
        exclude =['question']

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
