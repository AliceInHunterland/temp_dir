from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from .database import Base


class NFT(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True, index=True)
    tokenid = Column(String(255), unique=True)
    file_path = Column(String)
    param = Column(String)
