from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Recipient, ExceptModeDeliveryRule, FilterModeDeliveryRule
from .serializer import RecipientSerializer, ExceptModeDeliveryRuleSerializer, FilterModeDeliveryRuleSerializer


class RecipientView(APIView):

    def get(self, request):
        recipients = Recipient.objects.all()
        serializer = RecipientSerializer(recipients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecipientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipientDetailView(APIView):

    def get(self, request, pk):
        recipient = Recipient.objects.get(pk=pk)
        serializer = RecipientSerializer(recipient)
        return Response(serializer.data)

    def put(self, request, pk):
        recipient = Recipient.objects.get(pk=pk)
        request.data.setdefault('email', recipient.email)
        request.data.setdefault('name', recipient.name)

        serializer = RecipientSerializer(recipient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            recipient = Recipient.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        recipient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RuleView(APIView):

    def get(self, request):
        rules = self.model.objects.all()
        uid = request.query_params.get('uid')
        if uid is not None:
            rules = rules.filter(recipient=uid)
        serializer = self.serializer(rules, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExceptRuleView(RuleView):
    model = ExceptModeDeliveryRule
    serializer = ExceptModeDeliveryRuleSerializer


class FilterRuleView(RuleView):
    model = FilterModeDeliveryRule
    serializer = FilterModeDeliveryRuleSerializer
