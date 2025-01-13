# pendientes/serializers.py
from rest_framework import serializers
from .models import PendingApproval

class PendingApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingApproval
        fields = '__all__'
