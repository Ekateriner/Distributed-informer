from rest_framework import serializers
from .models import Recipient, FilterModeDeliveryRule, ExceptModeDeliveryRule


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = '__all__'


class FilterModeDeliveryRuleSerializer(serializers.ModelSerializer):
    recipient = RecipientSerializer()

    class Meta:
        model = FilterModeDeliveryRule
        fields = '__all__'


class ExceptModeDeliveryRuleSerializer(serializers.ModelSerializer):
    recipient = RecipientSerializer()

    class Meta:
        model = ExceptModeDeliveryRule
        fields = '__all__'
