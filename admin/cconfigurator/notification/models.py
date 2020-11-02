from django.db import models

from recipient.models import Recipient
from tag.models import Tag
from template_instance.models import TemplateInstance


class Notification(models.Model):
    user = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    template_instance = models.ForeignKey(
        TemplateInstance,
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"{self.user} - {self.template_instance}"
