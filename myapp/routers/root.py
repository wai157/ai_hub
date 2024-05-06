from flask import Blueprint, render_template
from database import models_db, tasks_db

router = Blueprint('root', __name__)

@router.route('/', methods=['GET'])
def index():
    models = models_db.get_models()
    tasks = tasks_db.get_tasks()
    return render_template('index.html',
                           models=models,
                           tasks=tasks)

@router.route('/health', methods=['GET'])
def health():
    return 'OK'