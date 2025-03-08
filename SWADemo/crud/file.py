from SWADemo.crud.base import CRUDBase
from SWADemo.models.file import File


class CRUDFile(CRUDBase):
    pass


crud_files = CRUDFile(File)
