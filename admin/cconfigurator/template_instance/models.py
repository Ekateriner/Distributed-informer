import hashlib
import json
import jsonfield
import logging
import requests

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from requests import HTTPError

from cconfigurator.settings import TASK_CREATOR_URL
from template.models import Template

logger = logging.getLogger(__name__)


class TemplateInstance(models.Model):
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
    )
    args = jsonfield.JSONField(blank=True)
    hash_args = models.CharField(max_length=32, blank=True, default="")
    task_id = models.CharField(max_length=100, blank=True, default="")
    level_id = models.CharField(max_length=100, blank=True, default="")
    info = models.FloatField()
    warn = models.FloatField()
    crit = models.FloatField()

    def clean(self):
        errors = []
        if not self.info < self.warn < self.crit:
            errors.append(ValidationError("It must be info < warn < crit"))

        for key in self.template.defaults.keys():
            if key not in self.args.keys():
                self.args[key] = self.template.defaults[key]

        args = list(self.template.args.keys())
        for key in self.args.keys():
            if key not in args:
                errors.append(ValidationError(f"Unknown argument: {key}"))
            else:
                args.remove(key)
        for key in args:
            errors.append(
                ValidationError(f"Missed value for argument: {key}")
            )

        self.hash_args = hashlib.md5(str(sorted(self.args.items())).encode()).hexdigest()

        try:
            template_instance = TemplateInstance.objects.get(
                template=self.template,
                info=self.info,
                warn=self.warn,
                crit=self.crit,
                hash_args=self.hash_args,
            )
        except ObjectDoesNotExist as exc:
            pass
        else:
            errors.append(
                ValidationError(f"Such template instance already exists: {template_instance.id}")
            )

        if len(errors) > 0:
            raise ValidationError(errors)

        task_data = {
            "template": self.template.data,
            "args": self.args,
            "info": self.info,
            "warn": self.warn,
            "crit": self.crit
        }
        try:
            response = requests.post(TASK_CREATOR_URL, data=json.dumps(task_data))
            response.raise_for_status()
        except requests.exceptions.ConnectionError as exc:
            logger.warning(f"Cannot create task: {exc}")
        except HTTPError as exc:
            logger.exception(exc)
        else:
            response_data = response.json()
            self.task_id = response_data["task_id"]
            self.level_id = response_data["level_id"]

    def __str__(self):
        return f"{self.template.name} - {self.id}"
