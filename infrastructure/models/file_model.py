from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# SQLAlchemy model for the File entity
class FileModel(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    filename = Column(String, unique=True, nullable=False)
    content = Column(LargeBinary)