import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UploadedFile(TimeStampedModel):
    file = models.FileField(upload_to="media/")
    name = models.CharField(max_length=255)
    size = models.PositiveIntegerField(null=True)


class Document(TimeStampedModel):
    session_id = models.CharField(max_length=255, db_index=True)
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
