from pathlib import Path
from fastapi import UploadFile, HTTPException
from config import settings
from uuid import uuid4


class ImageHelper:
    allowed_extension = settings.ALLOWED_IMAGE_EXTENSION
    max_image_size = settings.MAX_IMAGE_SIZE

    def __init__(self, image: UploadFile, image_path: Path):
        self.image = image
        self.image_path = image_path

    async def save_image(self) -> Path:
        extension = Path(self.image.filename or "").suffix.lower()

        if extension not in self.allowed_extension:
            raise HTTPException(
                status_code=400,
                detail="Unsupported image extension",
            )

        content = await self.image.read(self.max_image_size + 1)

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Empty file",
            )

        if len(content) > self.max_image_size:
            raise HTTPException(
                status_code=400,
                detail="Image is too large",
            )

        filename = f"{uuid4().hex}{extension}"
        file_path = self.image_path / filename

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(content)

        return file_path
