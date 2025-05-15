from rest_framework import serializers
from apps.models import Good


class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = '__all__'
