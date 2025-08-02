import uuid

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UploadedFile(TimeStampedModel):
    content_type = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=255)
    s3_key = models.CharField(max_length=500, unique=True)
    size = models.PositiveIntegerField(null=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)


class Document(TimeStampedModel):
    session_key = models.CharField(max_length=255, db_index=True)
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.PROTECT)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
