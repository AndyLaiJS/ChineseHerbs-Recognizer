from flask import Flask, request
from flask_cors import CORS

import numpy as np
import cv2
import torch
import json

from torchvision import models, transforms
from torch.autograd import Variable
import torchvision.models as models

from PIL import Image

from pymongo import MongoClient
from pymongo import collection

# MongoDB connection
cluster = MongoClient(
    "mongodb+srv://user9879:mhw2102@mhw2101.achrh.mongodb.net/ChineseHerbs?ssl=true&ssl_cert_reqs=CERT_NONE")
db = cluster["ChineseHerbs"]
collection = db["Herbs"]
collect = collection.find({})

for c in collect:
    print(c)

class_labels = 'herbs_classes.json'

# Read the json
with open(class_labels, 'r') as fr:
    json_classes = json.loads(fr.read())

app = Flask(__name__)
app.run(host='0.0.0.0')

# Allow
CORS(app)

PATH = "./torch_model.pt"


@app.route("/")
def hello_world():
    return "<p>I am ND</p>"


@app.route('/hello')
def hello():
    return 'Hello, World'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # "Capture" the POST image upload
        print("\nREQUEST IS:")
        print(request.files)
        file = request.files['file']

        if file:
            preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor()
            ])

            # Path to uploaded image
            np_img = np.fromfile(file, np.uint8)
            file = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            file = cv2.cvtColor(file, cv2.COLOR_BGR2RGB)
            # print(type(file))
            # PILLOW format right here (.convert)
            file = Image.fromarray(np.uint8(file)).convert('RGB')
            # print(type(file))
            img_tensor = preprocess(file)
            # print(img_tensor)
            # print(img_tensor.shape)

            labels = {int(key): value for (key, value)
                      in json_classes.items()}
            predicted = predict_image(img_tensor)
            print(labels[predicted.item()])

            result = collection.find_one({"label": labels[predicted.item()]})
            print("Result", result)

            return json.dumps({"label": labels[predicted.item()], "data": result["benefits"]})
        else:
            return "Bad file"


def predict_image(img):
    model = torch.load(PATH, map_location='cpu')
    model.eval()

    network_output = model(Variable(img.unsqueeze(0)))
    predicted_label = torch.argmax(network_output)
    return predicted_label
