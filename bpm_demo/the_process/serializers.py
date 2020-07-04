from rest_framework import serializers
from .models import ProcessForm, State


class ProcessFormSerializer(serializers.ModelSerializer):
    """Serializer for Guest object"""
    class Meta:
        model = ProcessForm
        fields = '__all__'
        read_only_Fields = ('id',)

class StateSerializer(serializers.ModelSerializer):
    """Serializer for Guest object"""
    class Meta:
        model = State
        fields = '__all__'
        read_only_Fields = ('id',)