import json

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TemplateInstance
from .serializer import TemplateInstanceDetailedSerializer
from .serializer import TemplateInstanceSerializer


class TemplateInstanceView(APIView):

    def get(self, request):
        instances = TemplateInstance.objects.all()
        template_name = request.query_params.get('template')
        task_id = request.query_params.get('task_id')
        if template_name is not None:
            instances = instances.filter(template__name=template_name)
        if task_id is not None:
            instances = instances.filter(task_id=task_id)
        serializer = TemplateInstanceDetailedSerializer(instances, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TemplateInstanceSerializer(data=request.data)
        if serializer.is_valid():
            template_instance = TemplateInstance(**serializer.validated_data)
            try:
                template_instance.clean()
            except ValidationError as exc:
                return Response(exc.messages, status=status.HTTP_400_BAD_REQUEST)
            else:
                template_instance.save()
                return Response({"id": template_instance.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateInstanceDetailView(APIView):

    def get(self, request, pk):
        instance = TemplateInstance.objects.get(pk=pk)
        serializer = TemplateInstanceDetailedSerializer(instance)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            instance = TemplateInstance.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
