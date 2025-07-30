import uuid

import factory

from django.contrib.auth import get_user_model

from apps.documents.models import UploadedFile, Document

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User
        skip_postgeneration_save = True


class UploadedFileFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"sample_file_{n}.pdf")
    file = factory.django.FileField(filename="sample.pdf", data=b"%PDF-1.4\n%Test PDF")
    size = factory.LazyAttribute(lambda o: len(o.file.read()))

    class Meta:
        model = UploadedFile


class DocumentFactory(factory.django.DjangoModelFactory):
    session_key = factory.Faker("uuid4")
    uploaded_file = factory.SubFactory(UploadedFileFactory)
    user = factory.SubFactory(UserFactory)
    uuid = factory.LazyFunction(uuid.uuid4)

    class Meta:
        model = Document
