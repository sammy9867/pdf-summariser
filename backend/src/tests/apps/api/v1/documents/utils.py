import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from faker import Faker
from ninja import Schema

from apps.documents.models import Document, UploadedFile

fake = Faker()


def dump_with_django_encoder(schema_cls: Schema, obj: models.Model) -> dict:
    return json.loads(
        json.dumps(
            schema_cls.model_validate(obj).model_dump(mode="python"),
            cls=DjangoJSONEncoder,
        )
    )


async def create_document(session_key: str) -> Document:
    uploaded_file = await UploadedFile.objects.acreate(
        name=fake.file_name(extension="pdf"),
        s3_key=str(fake.uuid4()),
        size=100,
    )
    return await Document.objects.acreate(
        session_key=session_key, uploaded_file=uploaded_file
    )
