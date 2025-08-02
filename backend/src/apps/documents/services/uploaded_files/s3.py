import os
import uuid

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone


def _get_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
        # Disable SSL verification for LocalStack
        use_ssl=False,
        verify=False,
    )


def _ensure_bucket_exists(s3_client) -> bool:
    try:
        s3_client.head_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    except ClientError as e:
        error_code = int(e.response["Error"]["Code"])
        if error_code == 404:
            s3_client.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)


def s3_upload_file(file: InMemoryUploadedFile) -> str:
    file_extension = os.path.splitext(file.name)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    s3_key = f"uploads/{unique_filename}"
    s3_client = _get_client()
    _ensure_bucket_exists(s3_client)

    try:
        _ensure_bucket_exists(s3_client)
    except ClientError as e:
        raise e

    try:
        file.seek(0)
        s3_client.upload_fileobj(
            file,
            settings.AWS_STORAGE_BUCKET_NAME,
            s3_key,
            ExtraArgs={
                "ContentType": file.content_type or "application/octet-stream",
                "Metadata": {
                    "original_name": file.name,
                    "created": str(timezone.now()),
                },
            },
        )
    except (ClientError, NoCredentialsError) as e:
        raise e

    return s3_key
