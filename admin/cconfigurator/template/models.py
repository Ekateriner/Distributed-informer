from django.core.exceptions import ValidationError
from django.db import models
import jsonfield


class Template(models.Model):
    name = models.CharField(max_length=100, unique=True)
    data = models.TextField(default="")
    args = jsonfield.JSONField(
        blank=True,
        default={"measurement": "", "field": ""},
    )
    defaults = jsonfield.JSONField(blank=True, default={"field": "value"})

    def clean(self):
        errors = []
        if "measurement" not in self.args.keys():
            errors.append(
                ValidationError("Arguments must contain measurement")
            )
        if "field" not in self.args.keys():
            errors.append(ValidationError("Arguments must contain field"))
        for key in self.defaults.keys():
            if key not in self.args.keys():
                errors.append(
                    ValidationError(f"Unknown argument in defaults: {key}")
                )
        if len(errors) > 0:
            raise ValidationError(errors)

    def __str__(self):
        return self.name
