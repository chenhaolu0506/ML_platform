import tensorflow as tf
from tensorflow.keras import layers, Sequential
from glob import glob
from tqdm import tqdm
import numpy as np
import cv2
import query


def build_model():
    model = Sequential([
        layers.Conv2D(filters=128, kernel_size=5, activation='relu', input_shape=(64, 64, 3)),
        layers.MaxPooling2D(strides=2),
        layers.BatchNormalization(),
        layers.Conv2D(filters=64, kernel_size=5, activation='relu'),
        layers.MaxPooling2D(strides=2),
        layers.BatchNormalization(),
        layers.Conv2D(filters=32, kernel_size=5, activation='relu'),
        layers.MaxPooling2D(strides=2),
        layers.BatchNormalization(),
        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.Dense(128, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model


def save_model(model):
    model.save('./model/CNN')


def train_model():
    query.set_training_status(True)
    model = build_model()
    images = []
    labels = []
    for name in tqdm(glob('./static/data/vehicles/*')):
        img = cv2.imread(name)
        img = cv2.resize(img, (64, 64))
        images.append(img / 255)
        labels.append(1)

    for name in tqdm(glob('./static/data/non-vehicles/*')):
        img = cv2.imread(name)
        img = cv2.resize(img, (64, 64))
        images.append(img / 255)
        labels.append(0)

    images = np.array(images)
    labels = np.array(labels)
    model.fit(images, labels, epochs=10, batch_size=64, validation_split=0.2)
    save_model(model)
    query.set_training_status(False)


def load_model(path):
    model = tf.keras.models.load_model(path)
    return model


def predict(image):
    image = cv2.resize(image, (64, 64))
    model = load_model('./model/CNN')
    image = np.divide(image, 255)
    pred = model.predict(np.reshape(image, (-1, 64, 64, 3)))
    return 'vehicle' if pred >= 0.5 else 'not vehicle'
