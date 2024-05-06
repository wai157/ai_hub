import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    SECRET_KEY = os.urandom(24)
    HF_TOKEN = os.getenv('HF_TOKEN')
    API_URL = "https://api-inference.huggingface.co/models"
    
if __name__ == '__main__':
    conf = Config()
    print(f"{conf.SECRET_KEY = }")
    print(f"{conf.HF_TOKEN = }")
    print(f"{conf.API_URL = }")
    