from sqlalchemy.orm import Session

from . import models, schemas
import os

UPLOAD_FOLDER = "./uploads"


# def get_token(db: Session, token_id: int):
#     return db.query(models.NFT).filter(models.NFT.id == token_id).first()


def get_token_by_tokenid(db: Session, tokenid: str):
    return db.query(models.NFT).filter(models.NFT.tokenid == tokenid).first()


def get_tokens(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.NFT).offset(skip).limit(limit).all()


def create_token(db: Session, token: schemas.NFT):
    db_token = models.NFT(tokenid=token.tokenid, file_path=token.file_path, param=token.param)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def update_token(db: Session, token: models.NFT):
    db_token = db.query(models.NFT).filter(models.NFT.tokenid == token.tokenid).first()
    if db_token:
        db_token.param = token.param
        db.commit()
        db.refresh(db_token)
    return db_token
