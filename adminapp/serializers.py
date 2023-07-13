from rest_framework import serializers
from .models import AccessKey
from authentication.models import CustomUser



class AccessKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessKey
        fields = '__all__'

    def create(self,validated_data):
         return AccessKey.objects.create(**validated_data)  


