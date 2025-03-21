from sqlmodel import Session, select

from SWADemo.crud.base import CRUDBase
from SWADemo.models.file import File
from SWADemo.models.user import User


class CRUDFile(CRUDBase):
    def get_user_files(self, db: Session, user: User):
        files = db.exec(select(File).where(File.uploaded_by == user.id)).all()
        return files


crud_files = CRUDFile(File)
