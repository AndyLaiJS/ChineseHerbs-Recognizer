from flask import Flask, request
from flask_cors import CORS
import numpy as np
import cv2
import torch

app = Flask(__name__)

# Allow
CORS(app)


@app.route("/")
def hello_world():
    return "<p>I am ND</p>"


@app.route('/hello')
def hello():
    return 'Hello, World'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("People people!")
        # "Capture" the POST image upload
        file = request.files['file']
        # Convert into np array
        npimg = np.fromfile(file, np.uint8)
        file = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        # Convert into Tensor
        torch_file = torch.from_numpy(file)
        print(torch_file)

    return "Hot damn, we got a POST request!!"
