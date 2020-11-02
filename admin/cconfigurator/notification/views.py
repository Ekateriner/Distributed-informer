from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from . import dumpdata
from .models import Notification
from .serializer import NotificationSerializer
from .serializer import NotificationDetailedSerializer

from django.db.models import signals
from django.dispatch import receiver


class NotificationView(APIView):
    def get(self, request):
        notifications = Notification.objects.all()
        user_name = request.query_params.get('user')
        template_name = request.query_params.get('template')
        tag_names = request.query_params.get('tags')
        task_id = request.query_params.get('task_id')
        if user_name is not None:
            notifications = notifications.filter(user__name=user_name)
        if template_name is not None:
            notifications = notifications.filter(
                template_instance__template__name=template_name
            )
        if tag_names is not None:
            for tag in tag_names.split(','):
                notifications = notifications.filter(tags__name=tag)
        if task_id is not None:
            notifications = notifications.filter(
                template_instance__task_id=task_id
            )
        serializer = NotificationDetailedSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationDetailView(APIView):

    def get(self, request, pk):
        notification = Notification.objects.get(pk=pk)
        serializer = NotificationDetailedSerializer(notification)
        return Response(serializer.data)

    def put(self, request, pk):
        notification = Notification.objects.get(pk=pk)
        request.data.setdefault('info', notification.info)
        request.data.setdefault('warn', notification.warn)
        request.data.setdefault('crit', notification.crit)

        serializer = NotificationSerializer(notification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@receiver(signals.post_save)
def dumpdata_post_save(sender, instance, **kwargs):
    dumpdata.dumpdata_post_save(sender, instance, **kwargs)


@receiver(signals.post_delete)
def dumpdata_post_delete(sender, instance, **kwargs):
    dumpdata.dumpdata_post_delete(sender, instance, **kwargs)
