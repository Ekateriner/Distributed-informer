import pytest
from django.core.exceptions import ValidationError

from template.models import Template
from template_instance.models import TemplateInstance


@pytest.mark.django_db
class TestValidation:
    @pytest.fixture
    def template(self):
        """
        Return template fixture
        :return: Template(name="name", data="data", args={"measurement": "", "field": ""}, defaults={"field": "value"})
        """
        template = Template(name="name", data="data")
        template.save()
        return template

    def test_info_warn_crit(self, template):
        template_instance = TemplateInstance(
            template=template,
            info=1,
            warn=0.5,
            crit=0.7,
            args={"measurement": "cpu"}
        )
        with pytest.raises(ValidationError) as exc:
            template_instance.clean()
        assert exc.value.messages == ["It must be info < warn < crit"]

    def test_missed_values(self, template):
        template_instance = TemplateInstance(
            template=template,
            args={"field": "field"},
            info=0,
            warn=0.5,
            crit=1,
        )
        with pytest.raises(ValidationError) as exc:
            template_instance.clean()
        assert exc.value.messages == ["Missed value for argument: measurement"]

    def test_unknown_key(self, template):
        template_instance = TemplateInstance(
            template=template,
            args={"unknown": "unknown", "field": "field", "measurement": "measurement"},
            info=0,
            warn=0.5,
            crit=1,
        )
        with pytest.raises(ValidationError) as exc:
            template_instance.clean()
        assert exc.value.messages == ["Unknown argument: unknown"]

    def test_intance_already_exists(self, template):
        template_instance_1 = TemplateInstance(
            template=template,
            args={"measurement": "cpu"},
            info=0,
            warn=0.5,
            crit=1,
        )
        template_instance_1.clean()
        template_instance_1.save()
        template_instance_2 = TemplateInstance(
            template=template,
            args={
                "field": "value",
                "measurement": "cpu",
            },
            info=0,
            warn=0.5,
            crit=1,
        )
        with pytest.raises(ValidationError) as exc:
            template_instance_2.clean()
        assert exc.value.messages == ["Such template instance already exists: 1"]
