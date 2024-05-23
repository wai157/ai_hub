from flask import current_app, Blueprint, render_template, request
from database import models_db
import requests
import json

router = Blueprint('models', __name__, url_prefix='/models')

@router.route('/<path:model_name>', methods=['GET'])
def get_model(model_name):
    model = models_db.get_model(model_name)
    return render_template('model.html', model=model)

@router.route('/<path:model_name>', methods=['POST'])
def compute(model_name):
    headers = {"Authorization": f"Bearer {current_app.config['HF_TOKEN']}"}
    base_url = current_app.config["API_URL"]
    url = base_url + "/" + model_name
    timeout = 120
    
    try:
        if model_name=="facebook/bart-large-cnn":
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
        
        elif model_name=="MIT/ast-finetuned-audioset-10-10-0.4593":
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
        
        elif model_name=="superb/hubert-large-superb-er":
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
            
        elif model_name=="google/vit-base-patch16-224":
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
        elif model_name=="meta-llama/Meta-Llama-3-8B-Instruct":
            chat = "<|begin_of_text|>"
            count = 1
            for text in request.json["input"][::-1]:
                chat += f"<|start_header_id|>{"user" if count%2 else "assistant"}<|end_header_id|>\n\n{text}<|eot_id|>"
                count+=1
            chat += "<|start_header_id|>assistant<|end_header_id|>\n\n"
            response = requests.post(
                url=url,
                headers=headers,
                json={
                    "inputs": chat
                },
                timeout=timeout
            )
            if response.status_code == 200:
                data = {
                    "type": "conversation",
                    "data": response.json()[0]['generated_text'].split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip(),
                }
        elif model_name=="openai/whisper-large-v3":
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
        elif model_name=="stabilityai/stable-diffusion-xl-base-1.0":
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
        elif model_name=="facebook/detr-resnet-50":
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
                    "data": boxes,
                }
        
        
        if response.status_code == 200:
            return json.dumps(data)
        elif response.status_code == 503:
                return "Model is loading, please try again later.", 503
        else:
            print(response)
            return "An error occurred.", 404
    except Exception as e:
        print(e)
        return "An error occurred.", 500