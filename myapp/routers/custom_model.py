from flask import session, Blueprint, render_template, request, url_for, redirect
from database import models_db, tasks_db
import requests
import json

router = Blueprint('custom_model', __name__, url_prefix='/custom-model')

@router.route('/generate', methods=['GET', 'POST'])
def generate():
    session.clear()
    if request.method == 'GET':
        models = models_db.get_models()
        tasks = tasks_db.get_tasks()
        return render_template('custom_model_gen.html',
                            models=models,
                            tasks=tasks)
    elif request.method == 'POST':
        data = dict(request.form)
        for key, val in data.items():
            session[key] = json.loads(val)
        return redirect(url_for("custom_model.model"))
    
@router.route('/', methods=['GET', 'POST'])
def model():
    if request.method == 'GET':
        if session.get('models') is None:
            return redirect(url_for("custom_model.generate"))
        model = {
            "name": "custom-model",
            "task": "custom task",
            "description": "Custom model",
            "input_type": session.get("input_types")[0],
            "output_type": session.get("output_types")[-1]
        }
        return render_template("model.html", model=model)
    if request.method == 'POST':
        return "ok", 203