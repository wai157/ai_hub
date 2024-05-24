from flask import session, Blueprint, render_template, request, url_for, redirect
from database import models_db, tasks_db
import requests
import json
import os

router = Blueprint('custom_model', __name__, url_prefix='/custom-model')

@router.route('/generate', methods=['GET', 'POST'])
def generate():
    session.clear()
    if request.method == 'GET':
        models = models_db.get_models()
        models = [model for model in models if model.input_type not in ["conversation", "image_classes"]]
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
        if session.get("models") is None:
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
        if request.headers.get("models") is None:
            return "Model not found!", 404
        models = json.loads(request.headers.get('models'))
        input_types = json.loads(request.headers.get("input-types"))
        output_types = json.loads(request.headers.get("output-types"))
        url = "http://127.0.0.1:3000"+url_for("models.compute", model_name=models[0])
        if input_types[0] == "text":
            data = request.json["input"]
            response = requests.post(
                url=url,
                json={"input": data}
            )
        elif input_types[0] == "image" or input_types[0] == "audio":
            file = request.files["input"].read()
            response = requests.post(
                url=url,
                files={"input": file}
            )
        models = models[1:]
        input_types = input_types[1:]
        output_types = output_types[1:]
        for model, input_type, output_type in zip(models, input_types, output_types):
            url = "http://127.0.0.1:3000"+url_for("models.compute", model_name=model)
            if input_type == "text":
                data = response.json()["data"]
                response = requests.post(
                    url=url,
                    json={"input": data}
                )
            elif input_type == "image" or input_type == "audio":
                file = response.json()["data"]
                file = bytearray(file)
                with open("temp_file", "wb") as f:
                    f.write(file)
                response = requests.post(
                    url=url,
                    files={"input": open("temp_file", "rb")}
                )
                os.remove("temp_file")
                    
            # print(response.json())
        
        return response.json()
            