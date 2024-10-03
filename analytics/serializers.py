from rest_framework import serializers
from .models import GeneralAnalytics
from datetime import datetime

class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralAnalytics
        fields = "__all__"

    def validate_start_date(self, value):
        if value.day != 1:
            raise serializers.ValidationError("Start date must be the 1st day of month.")
        
        if value > datetime.now().date():
            raise serializers.ValidationError("Start date cannont be in future.")
        
        return value