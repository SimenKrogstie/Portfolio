# Author: Simen Roko Krogstie 
# Email: simen.roko.krogstie@nmbu.no


import numpy as np
from torchvision import datasets, transforms
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import os


class Layer:
    def __init__(self, inputd, outputd):
        self.input_dim = inputd
        self.output_dim = outputd
        self.initialization_f()

    def initialization_f(self):
        self.W = np.random.randn(self.outputd, self.inputd) 
        self.b = np.random.randn(self.outputd) 

    def read_data(self, Weight , bias):
        self.W = Weight
        self.b = bias

    def forward(self, x):
        z = self.W @ x + self.b
        return np.maximum(0, z)


class Network:
    def __init__(self, inputd):
        self.layers: List[Layer] = []
        self.inputd = inputd

    def add_layer(self, outputd):
        new_layer = Layer(self.input_dim, outputd)
        self.layers.append(new_layer)
        self.inputd = outputd

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        for layer in self.layers:
            y = layer.forward(y)
        return y
    
    def predict(self, x: np.ndarray):
        y = self.evaluate(x)
        return np.argmax(y, axis=0)

    def read(self, layer_file_dict: Dict[int, Tuple[str, str]]):
        for layer_idx, filepaths in layer_file_dict.items():
            if layer_idx >= len(self.layers):
                raise IndexError(f"Layer index {layer_idx} out of range.")

            if not filepaths:
                continue  
            weight_filepath, bias_filepath = filepaths

            if not os.path.exists(weight_filepath) or not os.path.exists(bias_filepath):
                raise FileNotFoundError(f"File(s) not found: {weight_filepath}, {bias_filepath}")

            W = np.loadtxt(weight_filepath, delimiter='\t')
            b = np.loadtxt(bias_filepath, delimiter='\t')
            
            self.layers[layer_idx].read(W, b)

def get_mnist():
    return datasets.MNIST(root='./data', train=True, transform=transforms.ToTensor(), download=True)

def return_image(image_index, mnist_dataset):
    image, label = mnist_dataset[image_index]
    image_matrix = image[0].detach().numpy()
    return image_matrix.reshape(image_matrix.size), image_matrix, label

mnist_dataset = get_mnist()


fig, axes = plt.subplots(1, 5, figsize=(10, 5))
for i, ax in enumerate(axes.flat):
    x, image, label = return_image(i, mnist_dataset)
    ax.imshow(image, cmap='binary')
    ax.set_axis_off()
    ax.set_title(f"Label: {label}")


net_manager = Network(784) 


layer1 = net_manager.add_layer(512)  
layer2 = net_manager.add_layer(256)  
layer3 = net_manager.add_layer(10) 


file_paths_weights = {0: ("w_and_b/W_1.txt", "w_and_b/b_1.txt"),
					  1: ("w_and_b/W_2.txt", "w_and_b/b_2.txt"),
					  2: ("w_and_b/W_3.txt", "w_and_b/b_3.txt")}
net_manager.read(file_paths_weights)


fig, axes = plt.subplots(5, 6, figsize=(10, 5))
for i, ax in enumerate(axes.flat):
    x, image, label = return_image(np.random.randint(0, 60000), mnist_dataset)
    ax.imshow(image, cmap='binary')
    ax.set_axis_off()
    ax.set_title(f"Label: {label}, NN: {net_manager.predict(x)}")
    ax.set_title(f"Truth: {label}, NN: {net_manager.predict(x)}")


image_index = 19961
x, image, label = return_image(image_index, mnist_dataset) 

predict = net_manager.predict(x)
print(f"Predicted Output: {predict}")
print(f"Actual Output: {label}")
probabilities = net_manager.evaluate(x)
print(f"Probabilities: {probabilities.round(3)}")


plt.imshow(image, cmap='binary')
plt.title(f"Truth: {label}, NN: {predict}")
plt.show()