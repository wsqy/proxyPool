from .models import ProxyPool
from rest_framework import serializers


class ProxyPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProxyPool
        fields = "__all__"