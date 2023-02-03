# uvicorn app.main:app --reload
from typing import List
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, Response, UploadFile
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from . import crud, models, schemas
from .database import SessionLocal, engine

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tokens/", response_model=schemas.NFT)
def create_token(token: schemas.NFT, db: Session = Depends(get_db)):
    db_token = crud.get_token_by_tokenid(db, tokenid=token.tokenid)
    if db_token:
        return crud.update_token(db=db, token=token)
        # raise HTTPException(status_code=400, detail="Token already registered")
    return crud.create_token(db=db, token=token)


@app.get("/tokens/", response_model=List[schemas.NFT])
def read_tokens(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tokens = crud.get_tokens(db, skip=skip, limit=limit)
    if tokens is None:
        raise HTTPException(status_code=404, detail="Tokenss not found")
    return tokens


@app.get("/tokens/{tokenid}", response_model=schemas.NFT)
def read_item(tokenid: str, db: Session = Depends(get_db)):
    db_token = crud.get_token_by_tokenid(db, tokenid=tokenid)

    if db_token is None:
        raise HTTPException(status_code=404, detail="Token not found")
    json_compatible_item_data = jsonable_encoder(db_token)
    return JSONResponse(content=json_compatible_item_data)


UPLOAD_FOLDER = "./app/upload"
import os


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, db: Session = Depends(get_db)):
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    db_token = crud.get_token_by_tokenid(db, tokenid=filename)
    if db_token is None:
        crud.create_token(db=db, token=schemas.NFT(tokenid=filename, file_path=file_path))
    else:
        setattr(db_token, 'file_path', file_path)
        db.add(db_token)
        db.commit()
        db.refresh(db_token)

    return crud.get_token_by_tokenid(db, tokenid=filename)
    # return {"filename": file.filename}


@app.get("/download/{tokenid}")
async def download_file(tokenid: str, db: Session = Depends(get_db)):
    db_token = crud.get_token_by_tokenid(db, tokenid=tokenid)
    if db_token.file_path is not None:
        file_path = db_token.file_path
        with open(file_path, "rb") as f:
            file_data = f.read()
        return Response(content=file_data, media_type="application/octet-stream",
                        headers={"Content-Disposition": f"attachment;filename={file_path}"})
    else:
        raise HTTPException(status_code=404, detail="Token not found")
