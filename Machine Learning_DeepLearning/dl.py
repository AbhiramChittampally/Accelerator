def neuron(inputs, weights, bias):
    weighted_sum = 0

    for x, w in zip(inputs, weights):
        weighted_sum += x * w

    z = weighted_sum + bias

    return z


inputs = [1.0, 2.0]
weights = [0.5, -0.3]
bias = 0.1

output = neuron(inputs, weights, bias)

print(output)





import math


def sigmoid(z):
    return 1 / (1 + math.exp(-z))


def neuron(inputs, weights, bias):
    weighted_sum = 0

    for x, w in zip(inputs, weights):
        weighted_sum += x * w

    z = weighted_sum + bias
    activation = sigmoid(z)

    return z, activation


inputs = [1.0, 2.0]
weights = [0.5, -0.3]
bias = 0.1

z, output = neuron(inputs, weights, bias)

print("Weighted sum:", z)
print("Activated output:", output)






def relu(x):
    return max(0, x)


x1 = 1.0
x2 = 2.0

w1 = 0.5
w2 = -0.3
hidden_bias = 0.1

hidden_z = x1 * w1 + x2 * w2 + hidden_bias
hidden_output = relu(hidden_z)

output_weight = 0.8
output_bias = -0.2

output_z = hidden_output * output_weight + output_bias
prediction = relu(output_z)

print("Hidden z:", hidden_z)
print("Hidden activation:", hidden_output)
print("Output z:", output_z)
print("Prediction:", prediction)







import math


def relu(x):
    return max(0, x)


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def neuron(inputs, weights, bias, activation):
    weighted_sum = 0

    for x, w in zip(inputs, weights):
        weighted_sum += x * w

    z = weighted_sum + bias

    return activation(z)


def forward_pass(inputs):
    hidden_weights = [0.5, -0.3]
    hidden_bias = 0.1

    hidden_output = neuron(
        inputs,
        hidden_weights,
        hidden_bias,
        relu
    )

    output_weight = 0.8
    output_bias = -0.2

    output_z = (
        hidden_output * output_weight
        + output_bias
    )

    output = sigmoid(output_z)

    return output


inputs = [1.0, 2.0]

prediction = forward_pass(inputs)

print("Prediction:", prediction)






import numpy as np

x = np.array([2.0, 3.0, 4.0])

w = np.array([0.5, 1.0, -0.2])

b = 0.5

z = np.dot(w, x) + b

print(z)