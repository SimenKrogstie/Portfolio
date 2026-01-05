# Authors: Simen Roko Krogstie and Pavel Gulin
# Email: simen.roko.krogstie@nmbu.no and pavel.gulin@nmbu.no

import numpy as np

def sigma(y):
    return np.maximum(0 ,y)

def layer(x, W, b):
    return sigma(W @ x + b)

def NN(x, W_list, b_list):
    num_layers = len(W_list)
    for i in range(num_layers):
        x = layer(x, W_list[i], b_list[i])
    return x

n = [64, 128, 128, 128, 10]

W_list = [np.random.rand(n[i], n[i - 1]) for i in range(1, len(n))]
b_list = [np.random.rand(n[i]) for i in range(1, len(n))]
x = np.random.rand(64)

output = NN(x, W_list, b_list)

print("Output of the Neural Network function")
print(output)

print("\nDimensions of the weight matrixes")
for i in range(len(W_list)):
    print(f'Layer {i + 1}: {W_list[i].shape}')
