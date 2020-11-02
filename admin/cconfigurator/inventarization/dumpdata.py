import json
import logging
import requests

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry

from cconfigurator.settings import INVENTARIZATION_SENDER_URL

from notification.models import Notification
from recipient.models import Recipient
from tag.models import Tag
from template.models import Template
from template_instance.models import TemplateInstance

from inventarization.models import Node, Site
from inventarization.serializer import NodeSerializer, SiteSerializer

logger = logging.getLogger(__name__)


def dumpdata_post_save(sender, instance, **kwargs):
    updated = {}
    if sender is Node:
        serializer = NodeSerializer(instance)
        model = "node"
        data = serializer.data
        tag_key = data['name']
        tag_values = {k: v for k, v in dict(data).items() if k not in ['id', 'name']}
        updated[tag_key] = tag_values
    elif sender is Site:
        serializer = SiteSerializer(instance)
        model = "site"
        data = serializer.data
        tag_key = data['node_id']['name']
        tag_values = {k: v for k, v in dict(data['node_id']).items() if k not in ['id', 'name']}
        tag_values.update({k: v for k, v in dict(data).items() if k not in ['id', 'node_id']})
        updated[tag_key] = tag_values
    else:
        if not any(sender is cls for cls in (Session, User, LogEntry, Tag, Template,
                                             TemplateInstance, Recipient, Notification)):
            logger.exception(
                f"Unknown type of saved data."
                f"Cannot dump data of type {sender}"
            )
        return

    data = {
        "action": "save",
        "model": model,
        "data": updated,
    }

    try:
        requests.post(INVENTARIZATION_SENDER_URL, data=json.dumps(data))
    except requests.exceptions.ConnectionError as exc:
        logger.warning(f"Cannot dump data: {exc}")


def dumpdata_post_delete(sender, instance, **kwargs):
    if not any(sender is cls for cls in (Node, Site)):
        model = sender.model_name()
    else:
        if not any(sender is cls for cls in (Session, User, LogEntry)):
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
        requests.post(INVENTARIZATION_SENDER_URL, data=json.dumps(data))
    except requests.exceptions.ConnectionError as exc:
        logger.warning(f"Cannot dump data: {exc}")
