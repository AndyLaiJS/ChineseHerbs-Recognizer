import os
import cv2
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


class fruitification():

    """
    STEPS:
    1) Denote the file directory for Apples, Mangoes, Bananas, Grapes and Strawberries
    2) Label them with a dictionary. We'll use np.eye to handle the labelling into the training_data
    3) Training_data = []
    4) Count how many fruits for each Apples, Mangoes, etc...
    5) Shuffle the training_data
    6) Save it
    """

    # IMG_SIZE dictates the dimensions we wanna resize it into i.e. 50x50
    IMG_SIZE = 50

    # Directory of fruits
    AP = "fruits/apple"
    BN = "fruits/banana"
    GR = "fruits/grape"
    MG = "fruits/mango"
    ST = "fruits/strawberry"

    # Labels for fruits in numbers
    LABELS = {AP: 0, BN: 1, GR: 2, MG: 3, ST: 4}
    training_data = []
    counts = [0, 0, 0, 0, 0]

    def make_training_data(self):
        for label in self.LABELS:
            print(label)

            # Access the individual images inside each directory folder
            for f in tqdm(os.listdir(label)):
                try:
                    # Create the full path name here
                    path = os.path.join(label, f)
                    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    img = cv2.resize(img, (self.IMG_SIZE, self.IMG_SIZE))

                    # eye is identity matrix. self.LABELS[label] is just dictionary and key accessing
                    self.training_data.append(
                        [np.array(img), np.eye(5)[self.LABELS[label]]])

                    # Count each fruit
                    self.counts[self.LABELS[label]] += 1

                except:
                    pass

        # shuffling, cuz I heard it helps reduce the model from memorizing patterns
        np.random.shuffle(self.training_data)
        np.save("training_data.npy", self.training_data)
        print(len(self.training_data))

        # printing the count for each fruits
        for i in self.LABELS:
            print(i[7:], ":", self.counts[self.LABELS[i]])


fds = fruitification()
print("Making...")
fds.make_training_data()
