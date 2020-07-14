from rest_framework import serializers
from .models import State,CreateInspectionForm,FindingsForm,QuestionaireForm,WarningsForm,ApprovalForm,SWOForm


class StateSerializer(serializers.ModelSerializer):
    """Serializer for Guest object"""
    class Meta:
        model = State
        fields = '__all__'
        read_only_Fields = ('id',)

class CreateInspectionFormSerializer(serializers.ModelSerializer):
    """Serializer for Guest object"""
    class Meta:
        model = CreateInspectionForm
        fields = '__all__'
        read_only_Fields = ('id',)


class FindingsFormSerializer(serializers.ModelSerializer):
    """Serializer for Guest object"""
    class Meta:
        model = FindingsForm
        fields = '__all__'
        read_only_Fields = ('id',)



class QuestionaireFormSerializer(serializers.ModelSerializer):
    """Serializer for Guest object"""
    class Meta:
        model = QuestionaireForm
        fields = '__all__'
        read_only_Fields = ('id',)


class WarningsFormSerializer(serializers.ModelSerializer):
    """Serializer for Guest object"""
    class Meta:
        model = WarningsForm
        fields = '__all__'
        read_only_Fields = ('id',)


class SWOFormSerializer(serializers.ModelSerializer):
    """Serializer for Guest object"""
    class Meta:
        model = SWOForm
        fields = '__all__'
        read_only_Fields = ('id',)


class ApprovalFormSerializer(serializers.ModelSerializer):
    """Serializer for Guest object"""
    class Meta:
        model = ApprovalForm
        fields = '__all__'
        read_only_Fields = ('id',)