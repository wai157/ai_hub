from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from .config import Base


class Model(Base):
    __tablename__ = "models"

    name = Column(String(255), primary_key=True)
    task_name = Column(ForeignKey("tasks.name", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    description = Column(String(255))
    input_type = Column(String(255), nullable=False)
    output_type = Column(String(255), nullable=False)

    task = relationship("Task", back_populates="models")
    
    def serialize(self):
        return {
            "name": self.name,
            "task": self.task_name,
            "description": self.description,
            "input_type": self.input_type,
            "output_type": self.output_type,
        }
    
class Task(Base):
    __tablename__ = "tasks"

    name = Column(String(255), primary_key=True)

    models = relationship("Model", back_populates="task")
    
    def serialize(self):
        return {
            "name": self.name,
        }