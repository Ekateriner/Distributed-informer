import pytest
from django.core.exceptions import ValidationError

from template.models import Template


class TestValidation:
    def test_empty_args(self):
        template = Template(
            name="name",
            data="data",
            args={},
        )
        with pytest.raises(ValidationError):
            template.clean()

    def test_missing_measurement(self):
        template = Template(
            name="name",
            data="data",
            args={"field": "field"},
        )
        with pytest.raises(ValidationError):
            template.clean()

    def test_missing_field(self):
        template = Template(
            name="name",
            data="data",
            args={"measurement": "measurement"},
        )
        with pytest.raises(ValidationError):
            template.clean()

    def test_unknown_key(self):
        template = Template(
            name="name",
            data="data",
            defaults={"unknown": "unknown"},
        )
        with pytest.raises(ValidationError):
            template.clean()
