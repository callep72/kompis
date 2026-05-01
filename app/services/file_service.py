import os
import shutil
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.models import File
from app.config import settings

MAX_BYTES = 50 * 1024 * 1024  # 50 MB

ALLOWED_MIME = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}


def get_by_component(db: Session, component_id: int) -> list[File]:
    return db.query(File).filter(File.component_id == component_id).all()


async def save_upload(db: Session, component_id: int, file: UploadFile, file_type: str) -> File:
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(status_code=415, detail=f"Filtyp ej tillåten: {file.content_type}")

    dest_dir = os.path.join(settings.file_storage_path, "components", str(component_id))
    os.makedirs(dest_dir, exist_ok=True)

    dest_path = os.path.join(dest_dir, file.filename)
    # Avoid collisions
    base, ext = os.path.splitext(file.filename)
    counter = 1
    while os.path.exists(dest_path):
        dest_path = os.path.join(dest_dir, f"{base}_{counter}{ext}")
        counter += 1

    written = 0
    with open(dest_path, "wb") as out:
        while chunk := await file.read(1024 * 1024):
            written += len(chunk)
            if written > MAX_BYTES:
                out.close()
                os.remove(dest_path)
                raise HTTPException(status_code=413, detail="Filen är större än 50 MB")
            out.write(chunk)

    rel_path = os.path.relpath(dest_path, settings.file_storage_path)
    is_primary = file_type == "image" and not db.query(File).filter(
        File.component_id == component_id, File.file_type == "image", File.is_primary == True
    ).first()

    db_file = File(
        component_id=component_id,
        file_type=file_type,
        source="upload",
        filename=os.path.basename(dest_path),
        filepath=rel_path,
        mime_type=file.content_type,
        is_primary=is_primary,
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def delete_file(db: Session, file_id: int) -> bool:
    f = db.query(File).filter(File.id == file_id).first()
    if not f:
        return False
    full_path = os.path.join(settings.file_storage_path, f.filepath)
    if os.path.exists(full_path):
        os.remove(full_path)
    db.delete(f)
    db.commit()
    return True
