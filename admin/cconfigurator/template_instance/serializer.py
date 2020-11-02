from rest_framework import serializers

from template.serializer import TemplateSerializer

from .models import TemplateInstance


class TemplateInstanceDetailedSerializer(serializers.ModelSerializer):
    template = TemplateSerializer()

    class Meta:
        model = TemplateInstance
        fields = '__all__'


class TemplateInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TemplateInstance
        fields = '__all__'
