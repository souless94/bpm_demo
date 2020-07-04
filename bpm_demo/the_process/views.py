from rest_framework import viewsets
from . import serializers
from .models import ProcessForm, State


class ProcessFormViewSet(viewsets.ModelViewSet):
    """ Viewset for Content with all the methods """
    serializer_class = serializers.ProcessFormSerializer
    queryset = ProcessForm.objects.all()
    filterset_fields = '__all__'

class StateViewSet(viewsets.ModelViewSet):
    """ Viewset for Content with all the methods """
    serializer_class = serializers.StateSerializer
    queryset = State.objects.all()
    filterset_fields = '__all__'