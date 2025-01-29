import cv2
import os
import numpy as np
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from pathlib import Path
from .. import models, schemas
from ..database import get_db

router = APIRouter()

def process_image(image_data, output_path):
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image data")
    proxy_img = cv2.resize(img, (1920, 1080))
    return cv2.imwrite(output_path, proxy_img)

@router.post("/upload/", response_model=schemas.ImageMetadata)
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # ベースディレクトリを取得
        base_dir = Path(__file__).resolve().parent.parent
        images_dir = base_dir / "images"
        
        # 必要なディレクトリを作成
        original_dir = images_dir / "original"
        proxy_dir = images_dir / "proxy"
        original_dir.mkdir(parents=True, exist_ok=True)
        proxy_dir.mkdir(parents=True, exist_ok=True)

        # ファイルパスの設定
        original_path = str(original_dir / file.filename)
        proxy_path = str(proxy_dir / file.filename)

        # オリジナル画像の保存
        content = await file.read()
        with open(original_path, "wb") as f:
            f.write(content)

        # プロキシ画像の作成
        if not process_image(content, proxy_path):
            raise HTTPException(status_code=500, detail="Failed to process image")

        # データベースエントリの作成
        db_metadata = models.ImageMetadata(
            original_path=f"images/original/{file.filename}",
            proxy_path=f"images/proxy/{file.filename}",
            capture_date=datetime.now(),
            scene_description="Scene analysis result",
            similarity_score=0.0,
            created_at=datetime.now()
        )
        
        db.add(db_metadata)
        db.commit()
        db.refresh(db_metadata)
        return db_metadata
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/images/", response_model=List[schemas.ImageMetadata])
def get_images(db: Session = Depends(get_db)):
    return db.query(models.ImageMetadata).all()

@router.get("/images/{image_id}", response_model=schemas.ImageMetadata)
def get_image(image_id: int, db: Session = Depends(get_db)):
    image_data = db.query(models.ImageMetadata).filter(models.ImageMetadata.id == image_id).first()
    if not image_data:
        raise HTTPException(status_code=404, detail="Image not found")
    return image_data
