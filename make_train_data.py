import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn import metrics

knn = cv2.ml.KNearest_create()

def start(sample_size=25):
    train_data = generate_data(sample_size)
    labels = classify_label(train_data)
    power, nomal, short = binding_label(train_data, labels)
    if knn.train(train_data, cv2.ml.ROW_SAMPLE, labels) == True:
        print("training is successful")
    else:
        print("training is fail")
    return power, nomal, short

def run(new_data, power, normal, short):
    a = np.array([new_data])
    b = a.astype(np.float32)
    ret, results, neighbor, dist = knn.findNearest(b,5)
    print("predicted label : ", ret)
    return int(results[0][0])

def generate_data(num_samples, num_features=2):
    data_size = (num_samples, num_features)
    data = np.random.randint(0,40, size=data_size)
    return data.astype(np.float32)

def classify_label(train_data):
    labels=[]
    for data in train_data:
        if data[1] < data[0]-15:
            labels.append(2)
        elif data[1] >= (data[0]/2 + 15):
            labels.append(0)
        else:
            labels.append(1)
    return np.array(labels)

def binding_label(train_data, labels):
    power = train_data[labels==0]
    nomal = train_data[labels==1]
    short = train_data[labels==2]
    return power, nomal, short

def plot_data(po, no, sh):
    plt.figure(figsize=(10,6))
    plt.scatter(po[:,0], po[:,1], c='r', marker='s', s=50)
    plt.scatter(no[:,0], no[:,1], c='g', marker='^', s=50)
    plt.scatter(sh[:,0], sh[:,1], c='b', marker='o', s=50)
    plt.xlabel('x is second for alarm term')
    plt.ylabel('y is 10s for time to close eyes')
