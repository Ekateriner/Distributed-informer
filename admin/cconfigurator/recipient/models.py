from django.db import models


class Recipient(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=100,
        default="+7**********",
        blank=True,
    )
    telegram = models.CharField(max_length=100, default="-", blank=True)
    id_for_bot = models.IntegerField(blank=True, null=True)
    id_for_matrix = models.CharField(max_length=100, default="-", blank=True)
    email = models.EmailField(blank=True, null=True)

    slow_mode_delivery_rule = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class FilterModeDeliveryRule(models.Model):
    rule = models.TextField()
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)


class ExceptModeDeliveryRule(models.Model):
    rule = models.TextField()
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
