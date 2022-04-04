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

'''
collection.insert_many([{"cn_label": "黃連", "en_label": "Coptis", "benefits": "Coptis has antibacterial, antiviral, antipyretic, anticancer, immunomodulatory, spasmolytic, antidiarrheal, anti–gastric ulcer, hypoglycemic, antiinflammatory, antihypertensive, antiplatelet aggregation, antiarteriosclerosis, and antiarrhythmia activities"}, {"cn_label": "葛根", "en_label": "Pueraria", "benefits": "The root of the plant contains phytoestrogens, compounds that have estrogen-like effects. Pueraria mirifica is sometimes used as an anti-aging supplement or as a natural remedy for menopausal symptoms such as hot flashes and vaginal dryness."}, {"cn_label": "高良薑", "en_label": "Galangal", "benefits": "Nothing yet"}, {"cn_label": "附子", "en_label": "Aconite", "benefits": "Nothing yet"}, {"cn_label": "防己", "en_label": "Stephania tetrandra", "benefits": "Tetrandrine has immunosuppressive, anti-inflammatory, anti-bacterial and anti-amoeba, anti-tumor, and extensive anti-allergic effects"}, {"cn_label": "防風", "en_label": "Siler", "benefits": "Nothing yet"}, {"cn_label": "獨活", "en_label": "Angelica pubescens", "benefits": "The root, seed, and fruit are used to make medicine. Angelica is used for heartburn, intestinal gas (flatulence), loss of appetite (anorexia), arthritis, circulation problems, \"runny nose\" (respiratory catarrh), nervousness, plague, and trouble sleeping (insomnia)."}, {"cn_label": "生地黃", "en_label": "Rehmannia glutinosa", "benefits": "The root and parts that grow above the ground are used to make medicine. Rehmannia is commonly found in herbal combinations used in Traditional Chinese Medicine and Japanese Medicine. Rehmannia is used for diabetes, “tired blood” (anemia), fever, weakened bones (osteoporosis), and allergies; and as a general tonic."}, {"cn_label": "當歸", "en_label": "Angelica", "benefits": "Angelica is a plant. The root, seed, and fruit are used to make medicine. Angelica is used for heartburn, intestinal gas (flatulence), loss of appetite (anorexia), arthritis, circulation problems, \"runny nose\" (respiratory catarrh), nervousness, plague, and trouble sleeping (insomnia)."}, {"cn_label": "川芎", "en_label": "Lovage Rhizome", "benefits": "Lovage is a plant. The root and underground stem (rhizome) are used to make medicine. Lovage is used as “irrigation therapy” for pain and swelling (inflammation) of the lower urinary tract, for prevention of kidney stones, and to increase the flow of urine when urinary tract infections or fluid retention is present."}, {"cn_label": "川烏", "en_label": "Common Monkshood Mother Root", "benefits": "Nothing yet"}, {"cn_label": "川牛膝", "en_label": "Achyranthes", "benefits": "Indigestion. Achyranthes aspera has excellent Deepan (appetizer) and Pachan (digestive) properties because of which it helps improve digestive strength and reduce Ama in the body."}, {"cn_label": "赤芍", "en_label": "red peony", "benefits": "It is also used for viral hepatitis, liver cirrhosis, upset stomach, muscle cramps, “hardening of the arteries” (atherosclerosis), and to cause vomiting. Peony is also used for spasms, whooping cough (pertussis), epilepsy, nerve pain (neuralgia), migraine headache, and chronic fatigue syndrome (CFS)."}, {"cn_label": "蒼朮", "en_label": "Atractylodes", "benefits": "Atractylodes or Bai Zhu is a key herb in Chinese Medicine. This atractylodes supplement helps remove the accumulation of food, Phlegm and Qi ( energy ) and boosts the health of Spleen, eliminates fluid retention and offers long term digestive as well as weight goal management benefits."}, {"cn_label": "柴胡", "en_label": "Bupleurum", "benefits": "May help manage diabetes. Bupleurum may help prevent neuropathy, a common complication for people with either type 1 or 2 diabetes"}, {"cn_label": "草烏", "en_label": "Aconitum carmichaelii", "benefits": "Aconite is also used as a disinfectant, to treat wounds, and to promote sweating. Some people apply aconite to the skin in liniment as a “counterirritant” for treating facial pain, joint pain, and leg pain (sciatica)."}, {"cn_label": "巴戟天", "en_label": "Morinda", "benefits": "In TCM it is indicated in the case of kidney yang deficiency and associated impotence, weak tendons and bones, presence of wind and dampness."},
                       {"cn_label": "白朮", "en_label": "Atractylodes", "benefits": "Atractylodes or Bai Zhu is a key herb in Chinese Medicine. This atractylodes supplement helps remove the accumulation of food, Phlegm and Qi ( energy ) and boosts the health of Spleen, eliminates fluid retention and offers long term digestive as well as weight goal management benefits."}, {"cn_label": "白芷", "en_label": "Angelica", "benefits": "Angelica is a plant. The root, seed, and fruit are used to make medicine. Angelica is used for heartburn, intestinal gas (flatulence), loss of appetite (anorexia), arthritis, circulation problems, \"runny nose\" (respiratory catarrh), nervousness, plague, and trouble sleeping (insomnia)."}, {"cn_label": "白芍", "en_label": "white peony", "benefits": "The root of white peony, or bai shao, is a traditional Chinese remedy. According to scientific research, the herb may improve blood flow, pain, hyperpigmentation, and mood disorders. It might also help autoimmune conditions and increase estrogen levels."}, {"cn_label": "白附子", "en_label": "White Aconite", "benefits": "Extracts of Aconitum species have been given orally in traditional medicine to reduce fever associated with colds, pneumonia, laryngitis, croup, and asthma; for pain, inflammation, and high blood pressure; as a diuretic; to cause sweating; to slow heart rate; and for sedation."}, {"cn_label": "百部", "en_label": "Stemona tuberosa", "benefits": "Stemona tuberosa has long been used in Korean and Chinese medicine to ameliorate various lung diseases such as pneumonia and bronchitis."}, {"cn_label": "丹參", "en_label": "Red sage", "benefits": "In Traditional Chinese Medicine, red sage has been used for thousands of years for its heart-boosting, antioxidant properties. Researchers have described red sage as a potential “red light” to prevent the development of heart disease."}, {"cn_label": "苦參", "en_label": "Sophora flavescens", "benefits": "Sophora flavescens or Ku Shen, which in Chinese means “bitter root,” is an herb used in Traditional medicine to treat a wide variety of symptoms, with purported effects on the liver, intestinal tract, and skin. Lab and animal studies have shown that some compounds can kill cancer cells and help fight certain viruses."}, {"cn_label": "牛膝", "en_label": "Achyranthes", "benefits": "Achyranthes aspera has excellent Deepan (appetizer) and Pachan (digestive) properties because of which it helps improve digestive strength and reduce Ama in the body."}, {"cn_label": "乾薑", "en_label": "Dried Ginger", "benefits": "Dried ginger powder is an effective cure for indigestion, sore throat, cold and cough. It is used to treat nausea. Ginger's therapeutic properties help stimulate blood circulation, cleanse the bowels and kidneys, remove toxins from the body and nourish the skin."}, {"cn_label": "大黃", "en_label": "Rhubarb", "benefits": "Rhubarb contains chemicals that might help heal cold sores and reduce swelling. Rhubarb also contains fiber, which might help reduce cholesterol levels and affect stomach conditions"}, {"cn_label": "北沙參", "en_label": "Northern ginseng", "benefits": "American ginseng (Panax quinquefolius, L.) may boost energy, lower blood sugar and cholesterol levels, reduce stress, promote relaxation, treat diabetes, and manage sexual dysfunction in men."}, {"cn_label": "天麻", "en_label": "Gastrodia", "benefits": "Gastrodia elata Blume (G. elata) is a notable herbal plant that has been traditionally used to treat various conditions including headache, dizziness, spasm, epilepsy, stoke, amnesia, and other disorders in oriental countries for centuries ("}, {"cn_label": "馬勃", "en_label": "puffball", "benefits": "this herb has an extraordinary hemostasis that is not second to starch sponge or gelatin sponge. And it works on a variety of bleedings, such as oral bleeding, nose bleeding, traumatic hemorrhage, etc. More importantly, it is simple to use – tear the peridium, take out the sponge-like tissue, and then press against the bleeding part, stuff into bleeding nose, or fill the gums. Besides, its decoction cures swollen sore throat, hoarse voice, aphonia, and more."}])
'''

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

            result = collection.find_one(
                {"en_label": labels[predicted.item()]})
            print("Result", result)

            return json.dumps({"cnlabel": result["cn_label"], "label": labels[predicted.item()], "data": result["benefits"]})
        else:
            return "Bad file"


def predict_image(img):
    model = torch.load(PATH, map_location='cpu')
    model.eval()

    network_output = model(Variable(img.unsqueeze(0)))
    predicted_label = torch.argmax(network_output)
    return predicted_label
