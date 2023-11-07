import tensorflow as tf
import numpy as np

mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

def read(x, y):
    with open(x, 'r') as file:
        lines = file.readlines()
    count = 0
    line = []
    dx = []
    for i in range(len(lines)):
        line.append(eval(lines[i].strip()))
        count += 1
        if count == 56:
            count = 0
            dx.append(line)
            line = []
    dy = []
    with open(y, 'r') as file:
        lines = file.readlines()
    for line in lines:
        dy.append(int(line.strip()))
    return np.array(dx), np.array(dy)


model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(26, activation=tf.nn.softmax))

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
# model.build((None,) + (28, 28))
x_train, y_train = read("alphax", "alphay")
model.fit(x_train, y_train, epochs=100)

# val_loss, val_acc = model.evaluate(x_test, y_test)

model.save("alpha_one")
