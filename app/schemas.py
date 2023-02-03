from typing import List, Optional
from fastapi import UploadFile
from pydantic import BaseModel


class TokenBase(BaseModel):
    tokenid: str


class NFT(TokenBase):
    param: Optional[str]
    file_path: Optional[str]


    class Config:
        orm_mode = True

