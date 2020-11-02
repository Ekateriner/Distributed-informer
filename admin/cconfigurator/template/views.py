from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Template
from .serializer import TemplateSerializer


class TemplateView(APIView):

    def get(self, request):
        templates = Template.objects.all()
        template_name = request.query_params.get('template')
        if template_name is not None:
            templates = templates.filter(name=template_name)
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateDetailView(APIView):

    def get(self, request, pk):
        template = Template.objects.get(pk=pk)
        serializer = TemplateSerializer(template)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            template = Template.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
