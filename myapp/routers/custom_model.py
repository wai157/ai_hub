from flask import current_app, Blueprint, render_template, request
from database import models_db, tasks_db
import requests
import json

router = Blueprint('custom_model', __name__, url_prefix='/custom_model')

@router.route('/generate', methods=['GET'])
def generate():
    models = models_db.get_models()
    tasks = tasks_db.get_tasks()
    return render_template('custom_model_gen.html',
                           models=models,
                           tasks=tasks)