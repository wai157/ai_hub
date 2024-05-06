from .models import Model
from .config import SessionLocal

class Model_Mapper:
    def __init__(self, model: Model):
        for key, value in model.serialize().items():
            setattr(self, key, value)

def get_models():
    with SessionLocal() as session:
        db_models = session.query(Model).all()
        models = [Model_Mapper(model) for model in db_models]
        return models
    
def get_model(model_name):
    with SessionLocal() as session:
        db_model = session.query(Model).filter(Model.name == model_name).first()
        model = Model_Mapper(db_model)
        return model