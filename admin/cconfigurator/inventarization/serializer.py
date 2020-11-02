from rest_framework import serializers

from .models import *


class UplinkStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UplinkStat
        fields = '__all__'


class BorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Border
        fields = '__all__'


class SiteLatencySerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteLatency
        fields = '__all__'


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'


class SiteSerializer(serializers.ModelSerializer):
    node_id = NodeSerializer()

    class Meta:
        model = Site
        fields = '__all__'


class NodeLatencySerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeLatency
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class NodeIpSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeIp
        fields = '__all__'
