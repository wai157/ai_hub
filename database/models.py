from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .config import Base
   

class Model_Tag(Base):
    __tablename__ = "model_tags"

    model_id = Column(ForeignKey("models.id"), primary_key=True)
    tag = Column(ForeignKey("tags.tag"), primary_key=True)

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    input_type = Column(String(255), nullable=False)
    output_type = Column(String(255), nullable=False)

    tags = relationship("Tag", secondary="model_tags", back_populates="models")
    
class Tag(Base):
    __tablename__ = "tags"

    tag = Column(String(255), primary_key=True)

    models = relationship("Model", secondary="model_tags", back_populates="tags")