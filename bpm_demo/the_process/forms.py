from django.forms import ModelForm
from .models import Task , state

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('diagram',)

class StateForm(ModelForm):
    class Meta:
        model = state
        fields = '__all__'