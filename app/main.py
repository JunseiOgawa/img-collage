import os
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database
from fastapi.staticfiles import StaticFiles

# データベースの初期化
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# 静的ファイル用のディレクトリを作成
os.makedirs("media/task_images", exist_ok=True)
app.mount("/media", StaticFiles(directory="media"), name="media")

@app.post("/tasks/", response_model=schemas.Task)
async def create_task(
    title: str,
    image: UploadFile = File(None),
    db: Session = Depends(database.get_db)
):
    task = models.Task(title=title)
    
    if image:
        # 画像サイズチェック (200MB)
        if len(await image.read()) > 200 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image too large")
        await image.seek(0)
        
        # 画像を保存
        file_path = f"media/task_images/{image.filename}"
        with open(file_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
        task.image_path = f"/media/task_images/{image.filename}"
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(db: Session = Depends(database.get_db)):
    return db.query(models.Task).all()

@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
