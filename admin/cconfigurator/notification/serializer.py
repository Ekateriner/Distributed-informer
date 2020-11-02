from rest_framework import serializers

from .models import Notification
from recipient.serializer import RecipientSerializer
from tag.serializer import TagSerializer
from template_instance.serializer import TemplateInstanceDetailedSerializer


class NotificationDetailedSerializer(serializers.ModelSerializer):
    user = RecipientSerializer()
    template_instance = TemplateInstanceDetailedSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Notification
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
