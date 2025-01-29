from sqlalchemy import Column, Integer, String, DateTime, Float
from .database import Base

class ImageMetadata(Base):
    __tablename__ = "image_metadata"

    id = Column(Integer, primary_key=True, index=True)
    original_path = Column(String, unique=True, index=True)
    proxy_path = Column(String)
    capture_date = Column(DateTime)
    scene_description = Column(String)
    similarity_score = Column(Float)
    created_at = Column(DateTime)
