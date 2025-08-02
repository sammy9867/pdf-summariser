import uuid

import factory

from apps.documents.models import UploadedFile, Document


class UploadedFileFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"sample_file_{n}.pdf")
    s3_key = factory.Faker("uuid4")
    size = 100

    class Meta:
        model = UploadedFile


class DocumentFactory(factory.django.DjangoModelFactory):
    session_key = factory.Faker("uuid4")
    uploaded_file = factory.SubFactory(UploadedFileFactory)
    uuid = factory.LazyFunction(uuid.uuid4)

    class Meta:
        model = Document
