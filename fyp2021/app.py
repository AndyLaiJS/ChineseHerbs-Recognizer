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

# collection.insert_many([{"label": "Puffball", "benefits": ""}, {"label": "Gastrodia", "benefits": ""}, {"label": "Northern Ginseng", "benefits": ""}, {"label": "Rhubarb", "benefits": ""}, {"label": "Dried Ginger", "benefits": ""}, {"label": "Achyranthes", "benefits": ""}, {"label": "Sophora Flavescens", "benefits": ""}, {"label": "Red Sage", "benefits": ""}, {"label": "Stemona Tuberosa", "benefits": ""}, {"label": "White Aconite", "benefits": ""}, {"label": "white peony", "benefits": ""}, {"label": "Angelica", "benefits": ""}, {"label": "Atractylodes", "benefits": ""}, {"label": "Morinda", "benefits": ""}, {"label": "Aconitum Carmichaelii", "benefits": ""}, {"label": "Bupleurum", "benefits": ""}, {"label": "Atractylodes", "benefits": ""}, {"label": "Red Peony", "benefits": ""}, {"label": "Achyranthes", "benefits": ""}, {"label": "Common Monkshood Mother Root", "benefits": ""}, {"label": "Szechwan Lovage Rhizome", "benefits": ""}, {"label": "Angelica", "benefits": ""}, {"label": "Rehmannia Glutinosa", "benefits": ""}, {"label": "Angelica Pubescens", "benefits": ""}, {"label": "Windproof", "benefits": ""}, {"label": "Stephania Tetrandra", "benefits": ""}, {"label": "Aconite", "benefits": ""}, {"label": "Galangal", "benefits": ""}, {"label": "Pueraria", "benefits": ""}, {"label": "Coptis", "benefits": ""}, {"label": "Astragalus", "benefits": ""}, {"label": "Baikal Skullcap", "benefits": ""}, {"label": "Neopicrorhiza Scrophulariiflora", "benefits": ""}, {"label": "Bellflower", "benefits": ""}, {"label": "Reed Root", "benefits": ""}, {"label": "Dwarf Lilyturf", "benefits": ""}, {"label": "Saussurea Costus", "benefits": ""}, {"label": "Notopterygium Incisum", "benefits": ""}, {"label": "Whiteflower Hogfennel Root", "benefits": ""}, {"label": "Gentiana Macrophylla", "benefits": ""}, {"label": "Blackberry Lily", "benefits": ""}, {"label": "Cimicifuga", "benefits": ""}, {"label": "Japanese Sweet Flag", "benefits": ""}, {"label": "Asparagus", "benefits": ""}, {"label": "Trichosanthin", "benefits": ""}, {"label": "Lindera Aggregata", "benefits": ""}, {"label": "Cymbidium", "benefits": ""}, {"label": "Scallion White", "benefits": ""}, {"label": "Asarum", "benefits": ""}, {"label": "American Ginseng", "benefits": ""}, {"label": "Scrophularia", "benefits": ""}, {"label": "Corydalis Yanhusuo", "benefits": ""}, {"label": "Yuanzhi", "benefits": ""}, {"label": "Polygonatum", "benefits": ""}, {"label": "Common water-plantain", "benefits": ""}, {"label": "Anemarrhena", "benefits": ""}, {"label": "Aster", "benefits": ""}, {"label": "Licorice", "benefits": ""}, {"label": "Pinellia", "benefits": ""}, {"label": "ramulus cinnamomi", "benefits": ""}, {"label": "Chocolate Vine", "benefits": ""}, {"label": "Mulberry Mistletoe", "benefits": ""}, {"label": "White Lentils", "benefits": ""}, {"label": "Ginkgo", "benefits": ""},
#    {"label": "Piper", "benefits": ""}, {"label": "Betel Nut", "benefits": ""}, {"label": "Psoralea", "benefits": ""}, {"label": "Grass Cardamom", "benefits": ""}, {"label": "Grass Fruit", "benefits": ""}, {"label": "Chenpi", "benefits": ""}, {"label": "Psyllium", "benefits": ""}, {"label": "Red Bean", "benefits": ""}, {"label": "Arece Peel", "benefits": ""}, {"label": "Light Tempeh", "benefits": ""}, {"label": "Jujube", "benefits": ""}, {"label": "Gualou", "benefits": ""}, {"label": "Forsythia", "benefits": ""}, {"label": "Longan meat", "benefits": ""}, {"label": "Malt", "benefits": ""}, {"label": "Vitex", "benefits": ""}, {"label": "Papaya", "benefits": ""}, {"label": "Green Leather", "benefits": ""}, {"label": "Nutmeg", "benefits": ""}, {"label": "Hawthorn", "benefits": ""}, {"label": "peach kernel", "benefits": ""}, {"label": "Schisandra", "benefits": ""}, {"label": "Evodia", "benefits": ""}, {"label": "Cumin", "benefits": ""}, {"label": "Coix Seed", "benefits": ""}, {"label": "Citrus Aurantium", "benefits": ""}, {"label": "Citrus Aurantium", "benefits": ""}, {"label": "Gardenia", "benefits": ""}, {"label": "Goji Berries", "benefits": ""}, {"label": "Gorgon", "benefits": ""}, {"label": "cornelian cherry", "benefits": ""}, {"label": "Smoked plum", "benefits": ""}, {"label": "Neem", "benefits": ""}, {"label": "Burdock", "benefits": ""}, {"label": "Amomum", "benefits": ""}, {"label": "Mint", "benefits": ""}, {"label": "Cirsium Japonicum", "benefits": ""}, {"label": "Creeping Thistle", "benefits": ""}, {"label": "Fineleaf Schizonepeta Herb", "benefits": ""}, {"label": "Chinese Ephedrs Herb", "benefits": ""}, {"label": "Artemisia Annua", "benefits": ""}, {"label": "Dianthus Superbus", "benefits": ""}, {"label": "Dendrobium", "benefits": ""}, {"label": "Oriental Motherwort", "benefits": ""}, {"label": "Capillary Wormwood", "benefits": ""}, {"label": "Cloves", "benefits": ""}, {"label": "Honeysuckle", "benefits": ""}, {"label": "Common Coltsfoot Flower", "benefits": ""}, {"label": "Safflower", "benefits": ""}, {"label": "Inula flower", "benefits": ""}, {"label": "Arborvitae Leaf", "benefits": ""}, {"label": "Mulberry Leaf", "benefits": ""}, {"label": "Perilla Leaves", "benefits": ""}, {"label": "Lily", "benefits": ""}, {"label": "EEucommia Ulmoides", "benefits": ""}, {"label": "Peony Bark", "benefits": ""}, {"label": "Cinnamon", "benefits": ""}, {"label": "Mulberry White Bark", "benefits": ""}, {"label": "China Root", "benefits": ""}, {"label": "Myrrh", "benefits": ""}, {"label": "Frankincense", "benefits": ""}, {"label": "Rhus Rhinensis", "benefits": ""}, {"label": "Agarwood", "benefits": ""}, {"label": "Southern Dates", "benefits": ""}, {"label": "Codonopsis Pilosula", "benefits": ""}, {"label": "Tuber Fleeceflower", "benefits": ""}, {"label": "Rehmannia Glutinosa", "benefits": ""}])
collect = collection.find({})
print(collection.count_documents({}))

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
