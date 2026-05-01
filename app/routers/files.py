from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import file_service

router = APIRouter(prefix="/api/components/{component_id}/files", tags=["files"])


@router.post("", status_code=201)
async def upload_file(
    component_id: int,
    file: UploadFile = FastAPIFile(...),
    file_type: str = Form(default="image"),
    db: Session = Depends(get_db),
):
    return await file_service.save_upload(db, component_id, file, file_type)


@router.delete("/{file_id}", status_code=204)
def delete_file(component_id: int, file_id: int, db: Session = Depends(get_db)):
    if not file_service.delete_file(db, file_id):
        raise HTTPException(status_code=404, detail="Fil hittades inte")
