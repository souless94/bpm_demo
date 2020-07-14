from rest_framework import viewsets
from . import serializers
from .models import ProcessForm, State, CreateInspectionForm


class ProcessFormViewSet(viewsets.ModelViewSet):
    """ Viewset for Content with all the methods """
    serializer_class = serializers.ProcessFormSerializer
    queryset = ProcessForm.objects.all()
    filterset_fields = ['id',]

class StateViewSet(viewsets.ModelViewSet):
    """ Viewset for Content with all the methods """
    serializer_class = serializers.StateSerializer
    queryset = State.objects.all()
    filterset_fields = '__all__'

class CreateInspectionFormViewSet(viewsets.ModelViewSet):
    """ Viewset for Content with all the methods """
    serializer_class = serializers.CreateInspectionFormSerializer
    queryset = CreateInspectionForm.objects.all()
    filterset_fields = '__all__'