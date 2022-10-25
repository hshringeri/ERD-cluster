import cv2
import uuid
import os
import time
import random

labels = [ 'entity', 'relationship', 'weakEntitiy', 'identifyingRelationship', 'relationshipAttribute']

number_imgs = 10

a = []
for i in range(number_imgs):
    a.append(random.choice(os.listdir("AllData")))

print(a)

