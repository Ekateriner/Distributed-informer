import json
import logging
import requests

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry

from cconfigurator.config import SENDER_URL

from notification.models import Notification
from notification.serializer import NotificationSerializer

from recipient.models import Recipient
from recipient.serializer import RecipientSerializer

from tag.models import Tag
from tag.serializer import TagSerializer

from template.models import Template
from template.serializer import TemplateSerializer

from template_instance.models import TemplateInstance
from template_instance.serializer import TemplateInstanceSerializer

from inventarization.models import Node, Site

logger = logging.getLogger(__name__)


def dumpdata_post_save(sender, instance, **kwargs):
    if sender is Recipient:
        serializer = RecipientSerializer(instance)
        model = "recipient"
    elif sender is Notification:
        serializer = NotificationSerializer(instance)
        model = "notification"
    elif sender is Tag:
        serializer = TagSerializer(instance)
        model = "tag"
    elif sender is Template:
        serializer = TemplateSerializer(instance)
        model = "template"
    elif sender is TemplateInstance:
        serializer = TemplateInstanceSerializer(instance)
        model = "template_instance"
    else:
        if sender is not Session \
                and sender is not User \
                and sender is not LogEntry \
                and sender is not Node \
                and sender is not Site:
            logger.exception(
                f"Unknown type of saved data. "
                f"Cannot dump data of type {sender}"
            )
        return

    data = {
        "action": "save",
        "model": model,
        "data": serializer.data,
    }

    try:
        requests.post(SENDER_URL, data=json.dumps(data))
    except requests.exceptions.ConnectionError as exc:
        logger.warning(f"Cannot dump data: {exc}")


def dumpdata_post_delete(sender, instance, **kwargs):

    if sender is Recipient:
        model = "recipient"
    elif sender is Notification:
        model = "notification"
    elif sender is Tag:
        model = "tag"
    elif sender is Template:
        model = "template"
    elif sender is TemplateInstance:
        model = "template_instance"
    else:
        if sender is not Session \
                and sender is not User \
                and sender is not LogEntry:
            logger.exception(
                f"Unknown type of deleted data. "
                f"Cannot dump data of type {sender}"
            )
        return

    data = {
        "action": "delete",
        "model": model,
        "id": instance.pk,
    }

    try:
        requests.post(SENDER_URL, data=json.dumps(data))
    except requests.exceptions.ConnectionError as exc:
        logger.warning(f"Cannot dump data: {exc}")
