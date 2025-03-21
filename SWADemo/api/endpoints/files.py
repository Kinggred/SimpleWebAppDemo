import logging
from typing import Annotated, List
from uuid import UUID

import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlmodel import Session
import io

from starlette.responses import RedirectResponse

from SWADemo.api.auth import get_current_user
from SWADemo.crud.file import crud_files
from SWADemo.database import get_session
from SWADemo.models.file import FileView
from SWADemo.models.user import User


logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("", response_model=List[FileView])
def get_user_files(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_session)):
    return crud_files.get_user_files(db, current_user)


@router.get("/{file_id}", response_model=List[FileView])
def download_file(file_id: UUID, db: Session = Depends(get_session)):
    file = crud_files.get(db, file_id)
    s3_client = boto3.client("s3")

    try:
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": "swad-bucket", "Key": file.key},
            ExpiresIn=30,
            HttpMethod="GET"
        )

        return RedirectResponse(url=presigned_url)
    except Exception as e:
        logger.error(e)


@router.post("")
async def upload_file(file: UploadFile, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        s3_client = boto3.client("s3")
        s3_client.upload_fileobj(file.file, "swad-bucket", f"{current_user.id}_{file.filename}")
    except ClientError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return file.filename