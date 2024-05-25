from flask import session, current_app, Blueprint, render_template, request, url_for, redirect
from database import models_db
import requests
import json

router = Blueprint('models', __name__, url_prefix='/models')

@router.route('/<path:model_name>', methods=['GET'])
def get_model(model_name):
    model = models_db.get_model(model_name)
    if model:
        return render_template('model.html', model=model)
    else:
        return "Model not found!", 404

@router.route('/<path:model_name>', methods=['POST'])
def compute(model_name):
    headers = {"Authorization": f"Bearer {current_app.config['HF_TOKEN']}"}
    base_url = current_app.config["API_URL"]
    url = base_url + "/" + model_name
    timeout = 120
    
    try:
        if model_name == "custom-model":
            if session.get('models') is None:
                return "Model not found!", 404
            input_type = session.get("input_types")[0]
            headers.update({
                "models": json.dumps(session.get('models')),
                "input-types": json.dumps(session.get("input_types")),
                "output-types": json.dumps(session.get("output_types"))
            })
            if input_type == "text":
                response = requests.post(
                    url="http://127.0.0.1:3000"+url_for("custom_model.model"),
                    headers=headers,
                    json={
                        "input": request.json["input"]
                    },
                    timeout=timeout
                )
            elif input_type == "image" or input_type == "audio":
                file = request.files["input"].read()
                response = requests.post(
                    url="http://127.0.0.1:3000"+url_for("custom_model.model"),
                    headers=headers,
                    files={"input": file},
                    timeout=timeout
                )
            if response.status_code == 200:
                data = response.json()

        else:
            model = models_db.get_model(model_name)
            model_task = model.task
            
            if model_task == "Audio Classification":
                file = request.files["input"].read()
                response = requests.post(
                    url=url,
                    headers=headers,
                    data=file,
                    timeout=timeout
                )
                if response.status_code == 200:
                    data = {
                        "type": "classes",
                        "data": response.json(),
                    }
            
            elif model_task == "Automatic Speech Recognition":
                file = request.files["input"].read()
                response = requests.post(
                    url=url,
                    headers=headers,
                    data=file,
                    timeout=timeout
                )
                if response.status_code == 200:
                    output = response.json()["text"]
                    data = {
                        "type": "text",
                        "data": output,
                    }
                    
            elif model_task == "Chatbot":
                messages: list[dict] = []
                count = 1
                for text in request.json["input"][::-1]:
                    role = "user" if count%2 else "assistant"
                    content = text
                    messages.append({"role": role, "content": content})
                    count+=1
                response = requests.post(
                    url=url+"/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": model_name,
                        "messages": messages,
                        "stream": False
                    },
                    timeout=timeout
                )
                if response.status_code == 200:
                    data = {
                        "type": "conversation",
                        "data": response.json()["choices"][0]["message"]["content"],
                    }
            
            elif model_task == "Image Classification":
                file = request.files["input"].read()
                response = requests.post(
                    url=url,
                    headers=headers,
                    data=file,
                    timeout=timeout
                )
                if response.status_code == 200:
                    data = {
                        "type": "classes",
                        "data": response.json(),
                    }
            
            elif model_task == "Image to Text":
                file = request.files["input"].read()
                response = requests.post(
                    url=url,
                    headers=headers,
                    data=file,
                    timeout=timeout
                )
                if response.status_code == 200:
                    output = response.json()[0]["generated_text"]
                    data = {
                        "type": "text",
                        "data": output,
                    }
            
            elif model_task == "Object Detection":
                file = request.files["input"].read()
                response = requests.post(
                    url=url,
                    headers=headers,
                    data=file,
                    timeout=timeout
                )
                if response.status_code == 200:
                    boxes = response.json()
                    for box in boxes:
                        box["box"]["width"] = box["box"]["xmax"] - box["box"]["xmin"]
                        box["box"]["height"] = box["box"]["ymax"] - box["box"]["ymin"]
                    data = {
                        "type": "image_classes",
                        "data": {
                            "image": list(file),
                            "boxes": boxes
                        },
                    }
                    
            elif model_task == "Summarization":
                response = requests.post(
                    url=url,
                    headers=headers,
                    json={
                        "inputs": request.json["input"]
                    },
                    timeout=timeout
                )
                if response.status_code == 200:
                    output = response.json()[0]["summary_text"]
                    data = {
                        "type": "text",
                        "data": output,
                    }
            
            elif model_task == "Text Classification":
                response = requests.post(
                    url=url,
                    headers=headers,
                    json={
                        "inputs": request.json["input"]
                    },
                    timeout=timeout
                )
                if response.status_code == 200:
                    data = {
                        "type": "classes",
                        "data": response.json()[0],
                    }
                    
            elif model_task == "Text Generation":
                response = requests.post(
                    url=url,
                    headers=headers,
                    json={
                        "inputs": request.json["input"]
                    },
                    timeout=timeout
                )
                if response.status_code == 200:
                    output = response.json()[0]["generated_text"]
                    data = {
                        "type": "text",
                        "data": output,
                    }
            
            elif model_task == "Text to Image":
                response = requests.post(
                    url=url,
                    headers=headers,
                    json={
                        "inputs": request.json["input"]
                    },
                    timeout=timeout
                )
                if response.status_code == 200:
                    output = response.content
                    output = list(output)
                    data = {
                        "type": "image",
                        "data": output,
                    }
            
            elif model_task == "Translation":
                response = requests.post(
                    url=url,
                    headers=headers,
                    json={
                        "inputs": request.json["input"]
                    },
                    timeout=timeout
                )
                if response.status_code == 200:
                    output = response.json()[0]["translation_text"]
                    data = {
                        "type": "text",
                        "data": output,
                    }
                    
        
        if response.status_code == 200:
            return json.dumps(data)
        elif response.status_code == 503:
                return "Model is loading, please try again later.", 503
        else:
            return "An error occurred.", 404
    except Exception as e:
        print(e)
        return "An error occurred.", 500