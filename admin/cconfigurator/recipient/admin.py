from django.contrib import admin
from .models import Recipient, ExceptModeDeliveryRule, FilterModeDeliveryRule

admin.site.register(Recipient)
admin.site.register(ExceptModeDeliveryRule)
admin.site.register(FilterModeDeliveryRule)
