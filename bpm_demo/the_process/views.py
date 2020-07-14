from rest_framework import viewsets
from . import serializers
from .models import State,CreateInspectionForm,FindingsForm,QuestionaireForm,WarningsForm,ApprovalForm,SWOForm



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

class FindingsFormViewSet(viewsets.ModelViewSet):
    """ Viewset for Content with all the methods """
    serializer_class = serializers.FindingsFormSerializer
    queryset = FindingsForm.objects.all()
    filterset_fields = '__all__'

class QuestionaireFormViewSet(viewsets.ModelViewSet):
    """ Viewset for Content with all the methods """
    serializer_class = serializers.QuestionaireFormSerializer
    queryset = QuestionaireForm.objects.all()
    filterset_fields = '__all__'

class WarningsFormViewSet(viewsets.ModelViewSet):
    """ Viewset for Content with all the methods """
    serializer_class = serializers.WarningsFormSerializer
    queryset = WarningsForm.objects.all()
    filterset_fields = '__all__'

class SWOFormViewSet(viewsets.ModelViewSet):
    """ Viewset for Content with all the methods """
    serializer_class = serializers.SWOFormSerializer
    queryset = SWOForm.objects.all()
    filterset_fields = '__all__'

class ApprovalFormViewSet(viewsets.ModelViewSet):
    """ Viewset for Content with all the methods """
    serializer_class = serializers.ApprovalFormSerializer
    queryset = ApprovalForm.objects.all()
    filterset_fields = '__all__'