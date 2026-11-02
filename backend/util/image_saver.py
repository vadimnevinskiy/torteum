from pathlib import Path
from io import BytesIO
from uuid import uuid4

import aiofiles
from fastapi import UploadFile, HTTPException
from PIL import Image, UnidentifiedImageError

from config import settings


class ImageHelper:
    allowed_extension = settings.ALLOWED_IMAGE_EXTENSION
    allowed_format = settings.ALLOWED_FORMAT
    max_image_size = settings.MAX_IMAGE_SIZE

    def __init__(self, image: UploadFile, image_path: Path):
        self.image = image
        self.image_path = image_path

    async def save_image(self) -> str:
        extension = await self._get_extension()
        await self.image.seek(0)
        content = await self._read_content()
        self._validate_image(content)

        filename = f"{uuid4().hex}{extension}"
        await self._write_file(filename, content)

        return filename

    async def _write_file(self, filename: str, content: bytes):
        self.image_path.parent.mkdir(parents=True, exist_ok=True)
        file_path = self.image_path / filename
        async with aiofiles.open(file_path, mode="wb") as f:
            await f.write(content)

    async def _get_extension(self) -> str:
        extension = Path(self.image.filename or "").suffix.lower()

        if extension not in self.allowed_extension:
            raise HTTPException(
                status_code=400,
                detail="Unsupported image extension",
            )

        return extension

    async def _read_content(self):
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

        return content

    def _validate_image(self, content: bytes):
        try:
            with Image.open(BytesIO(content)) as image:
                image.verify()
                image_format = image.format
        except (UnidentifiedImageError, OSError):
            raise HTTPException(
                status_code=400,
                detail="Invalid image file",
            )

        if image_format not in self.allowed_format:
            raise HTTPException(
                status_code=400,
                detail="Unsupported image format",
            )
