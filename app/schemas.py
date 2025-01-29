from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ImageMetadataBase(BaseModel):
    original_path: str
    proxy_path: str
    capture_date: datetime
    scene_description: str
    similarity_score: float

class ImageMetadataCreate(ImageMetadataBase):
    pass

class ImageMetadata(ImageMetadataBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
