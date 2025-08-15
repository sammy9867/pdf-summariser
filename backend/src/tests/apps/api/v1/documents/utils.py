import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from ninja import Schema


def dump_with_django_encoder(schema_cls: Schema, obj: models.Model):
    return json.loads(
        json.dumps(
            schema_cls.model_validate(obj).model_dump(mode="python"),
            cls=DjangoJSONEncoder,
        )
    )
