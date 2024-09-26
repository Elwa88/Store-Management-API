from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        user = CustomUser(username = validated_data['username'],
                          role = validated_data['role'],
                          first_name = validated_data['first_name'],
                          last_name = validated_data['last_name'],)
        
        user.set_password(validated_data['password'])
        user.save()
        return user