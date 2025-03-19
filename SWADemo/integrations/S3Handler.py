from io import BytesIO
from typing import List, cast
from uuid import UUID

import boto3
from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools.utilities.parser.models import S3RecordModel
from sqlmodel import Session

from SWADemo.crud.file import crud_files
from SWADemo.crud.user import crud_users
from SWADemo.database import get_conn
from SWADemo.models.file import FileCreate
from SWADemo.models.S3File import S3File
from SWADemo.models.user import User


class S3Handler:
    def __init__(self, event):
        self.s3_client = boto3.client("s3")
        record: S3RecordModel = parse(model=S3RecordModel, event=event)
        self.bucket: str = record.s3.bucket.name
        self.file: S3File = S3File(key=record.s3.object.key)

    def upload_file(self, data: bytes, uploaded_by: UUID, filename: str):
        temp_file = BytesIO()
        temp_file.seek(0)
        # boto3.client('s3').upload_file(temp_file, bucket_name, 'folder/index.html')

        self.s3_client.upload_file(f"/store/{filename}", "demo", filename)

    def download_file(self, file: S3File) -> S3File:
        response = self.s3_client.get_object(Bucket=self.bucket, Key=file.key)
        file.data = response["Body"].read()
        return file

    def handle_event(self):
        with get_conn() as db:
            crud_users.get(db, self.file.uploaded_by)
            db_file = FileCreate(uploaded_by=self.file.uploaded_by, key=self.file.key, name=self.file.name)
            crud_files.create(db, db_file)
