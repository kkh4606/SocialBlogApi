from fastapi import UploadFile, File,  Depends, HTTPException, APIRouter
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app import database, oauth2
from app.images import imagekit
from app.models import User
import tempfile,os, shutil



router = APIRouter()
@router.put("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user: User = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(file.filename)[1]
        ) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        upload_result = imagekit.upload_file(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"],
            ),
        )

        if upload_result.response_metadata.http_status_code != 200:
            raise HTTPException(status_code=400, detail="Upload failed")


        user.profile_pic = upload_result.url

        db.commit()
        db.refresh(user)

        return user

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
