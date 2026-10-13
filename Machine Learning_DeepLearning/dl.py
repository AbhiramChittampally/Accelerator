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







import numpy as np


def relu(x):
    return np.maximum(0, x)


x = np.array([2.0, 3.0, 4.0])

w = np.array([0.5, 1.0, -0.2])

b = 0.5

z = np.dot(w, x) + b

a = relu(z)

print("Weighted sum:", z)
print("Activated output:", a)









import numpy as np


# -----------------------------
# ACTIVATION FUNCTIONS
# -----------------------------

def relu(x):
    return np.maximum(0, x)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# -----------------------------
# INPUT
# -----------------------------

X = np.array([
    [2.0, 3.0, 4.0],
    [1.0, 5.0, 2.0]
])


# -----------------------------
# WEIGHTS
# -----------------------------

W = np.array([
    [0.5, 0.2],
    [1.0, -0.4],
    [-0.2, 0.7]
])


# -----------------------------
# BIAS
# -----------------------------

b = np.array([0.5, -0.1])


# -----------------------------
# LINEAR TRANSFORMATION
# -----------------------------

Z = X @ W + b


# -----------------------------
# ACTIVATION
# -----------------------------

A = relu(Z)


print("Z:")
print(Z)

print("Activated output:")
print(A)





import numpy as np


def relu(x):
    return np.maximum(0, x)


# Input
X = np.array([[2.0, 3.0]])


# Layer 1 parameters
W1 = np.array([
    [0.5, 0.2, 0.1],
    [0.4, 0.8, 0.3]
])

b1 = np.array([0.1, 0.2, 0.1])


# Layer 2 parameters
W2 = np.array([
    [0.3, 0.5],
    [0.7, 0.2],
    [0.4, 0.6]
])

b2 = np.array([0.1, 0.2])


# Output layer parameters
W3 = np.array([
    [0.5],
    [0.8]
])

b3 = np.array([0.1])


# Forward pass
Z1 = X @ W1 + b1
A1 = relu(Z1)

Z2 = A1 @ W2 + b2
A2 = relu(Z2)

Z3 = A2 @ W3 + b3


print("Layer 1 output:")
print(A1)

print("Layer 2 output:")
print(A2)

print("Final output:")
print(Z3)





import numpy as np


# -----------------------------
# ACTIVATION
# -----------------------------

def relu(x):
    return np.maximum(0, x)


# -----------------------------
# INPUT
# -----------------------------

X = np.array([
    [2.0, 3.0],
    [4.0, 5.0]
])


# -----------------------------
# LAYER 1
# -----------------------------

W1 = np.array([
    [0.5, 0.2, 0.1],
    [0.4, 0.8, 0.3]
])

b1 = np.array([0.1, 0.2, 0.1])


# -----------------------------
# LAYER 2
# -----------------------------

W2 = np.array([
    [0.3, 0.5],
    [0.7, 0.2],
    [0.4, 0.6]
])

b2 = np.array([0.1, 0.2])


# -----------------------------
# OUTPUT LAYER
# -----------------------------

W3 = np.array([
    [0.5],
    [0.8]
])

b3 = np.array([0.1])


# -----------------------------
# FORWARD PASS
# -----------------------------

Z1 = X @ W1 + b1
A1 = relu(Z1)

Z2 = A1 @ W2 + b2
A2 = relu(Z2)

Z3 = A2 @ W3 + b3


# -----------------------------
# OUTPUT
# -----------------------------

print("Final output:")
print(Z3)





def gradient_descent_step(weight, gradient, learning_rate):
    return weight - (learning_rate * gradient)








def gradient_descent_step(weight, gradient, learning_rate):
    return weight - learning_rate * gradient


weight = 0.0
learning_rate = 0.1

for step in range(10):

    gradient = weight - 2.0

    weight = gradient_descent_step(
        weight,
        gradient,
        learning_rate
    )

    print(
        f"Step {step}: "
        f"Gradient = {gradient:.4f}, "
        f"Weight = {weight:.4f}"
    )
    
    
    
    
    







import torch

x = torch.tensor(2.0, requires_grad=True)

y = x ** 2

y.backward()

print("Value of x:", x.item())
print("Value of y:", y.item())
print("Gradient:", x.grad.item())









for epoch in range(epochs):

    optimizer.zero_grad()

    predictions = model(inputs)

    loss = loss_function(
        predictions,
        targets
    )

    loss.backward()

    optimizer.step()

    print(
        f"Epoch {epoch}: "
        f"Loss = {loss.item():.4f}"
    )
    
    
    
    
    
    
    
    
    
    
    
    
def mse_loss(y_true, y_pred):

    n = len(y_true)

    total = sum(
        (yt - yp) ** 2
        for yt, yp in zip(y_true, y_pred)
    )

    return total / n




   





def mse_loss(y_true, y_pred):
    n = len(y_true)

    total = sum(
        (yt - yp) ** 2
        for yt, yp in zip(y_true, y_pred)
    )

    return total / n


true_prices = [50, 65, 40]
predicted_prices = [48, 70, 44]

loss = mse_loss(true_prices, predicted_prices)

print("MSE:", loss)





import math

def binary_cross_entropy_loss(y_true, y_pred_prob):

    epsilon = 1e-9

    y_pred_prob = min(
        max(y_pred_prob, epsilon),
        1 - epsilon
    )

    return -(
        y_true * math.log(y_pred_prob)
        + (1 - y_true) * math.log(1 - y_pred_prob)
    )
    
    
    
    
    
    
    
    
    
    




import math


def binary_cross_entropy_loss(y_true, y_pred_prob):

    epsilon = 1e-9

    y_pred_prob = min(
        max(y_pred_prob, epsilon),
        1 - epsilon
    )

    return -(
        y_true * math.log(y_pred_prob)
        + (1 - y_true) * math.log(1 - y_pred_prob)
    )


loss_correct = binary_cross_entropy_loss(
    y_true=1,
    y_pred_prob=0.9
)

loss_wrong = binary_cross_entropy_loss(
    y_true=1,
    y_pred_prob=0.1
)

print("Correct prediction loss:", loss_correct)
print("Wrong prediction loss:", loss_wrong)







import torch
import torch.nn as nn

loss_function = nn.MSELoss()

actual = torch.tensor([10.0, 20.0, 30.0])
predicted = torch.tensor([12.0, 18.0, 29.0])

loss = loss_function(predicted, actual)

print(loss)





import torch
import torch.nn as nn

loss_function = nn.CrossEntropyLoss()

predictions = torch.tensor([
    [2.0, 1.0, 0.1],
    [0.1, 2.5, 0.3]
])

actual = torch.tensor([0, 1])

loss = loss_function(predictions, actual)

print(loss)








import torch
import torch.nn as nn

model = nn.Linear(1, 1)

loss_function = nn.MSELoss()

optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.01
)

x = torch.tensor([[1.0], [2.0], [3.0]])
y = torch.tensor([[2.0], [4.0], [6.0]])

for epoch in range(100):

    predictions = model(x)

    loss = loss_function(predictions, y)

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

print("Final Loss:", loss.item())









# Regression
import torchimport torch.nn as nnmodel = nn.Linear(1, 1)loss_function = nn.MSELoss()predictions = model(inputs)loss = loss_function(predictions, targets)


# Binary classification
import torchimport torch.nn as nnloss_function = nn.BCEWithLogitsLoss()logits = model(inputs)loss = loss_function(logits, targets)



# Multi-class classification
import torchimport torch.nn as nnloss_function = nn.CrossEntropyLoss()logits = model(inputs)loss = loss_function(logits, targets)











import torch

# Create input data
inputs = torch.tensor([
    [1.0, 2.0, 3.0, 4.0],
    [5.0, 6.0, 7.0, 8.0]
])

# Create weights
weights = torch.rand(4, 3)

# Create bias
bias = torch.rand(3)

# Calculate weighted sums
z = inputs @ weights + bias

print("Input shape:", inputs.shape)
print("Weight shape:", weights.shape)
print("Bias shape:", bias.shape)
print("Output shape:", z.shape)










import torch

# ==============================
# 1. DEVICE
# ==============================

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Device:", device)


# ==============================
# 2. CREATE TENSORS
# ==============================

scalar = torch.tensor(7.0)

vector = torch.tensor([1.0, 2.0, 3.0])

matrix = torch.tensor([
    [1.0, 2.0],
    [3.0, 4.0]
])


# ==============================
# 3. CHECK TENSOR INFORMATION
# ==============================

print("Scalar:", scalar)
print("Scalar shape:", scalar.shape)
print("Scalar dtype:", scalar.dtype)

print("Vector:", vector)
print("Vector shape:", vector.shape)
print("Vector dtype:", vector.dtype)

print("Matrix:", matrix)
print("Matrix shape:", matrix.shape)
print("Matrix dtype:", matrix.dtype)


# ==============================
# 4. CREATE COMMON TENSORS
# ==============================

zeros = torch.zeros(2, 3)

ones = torch.ones(2, 3)

random_tensor = torch.rand(2, 3)

sequence = torch.arange(0, 10)


# ==============================
# 5. RESHAPING
# ==============================

reshaped = ones.reshape(3, 2)

print("Original shape:", ones.shape)
print("Reshaped shape:", reshaped.shape)


# ==============================
# 6. ELEMENT-WISE OPERATIONS
# ==============================

a = torch.tensor([
    [1.0, 2.0],
    [3.0, 4.0]
])

b = torch.tensor([
    [5.0, 6.0],
    [7.0, 8.0]
])

addition = a + b

elementwise_multiplication = a * b


# ==============================
# 7. MATRIX MULTIPLICATION
# ==============================

matrix_multiplication = a @ b

print("Matrix multiplication:")
print(matrix_multiplication)

print("Result shape:", matrix_multiplication.shape)


# ==============================
# 8. MOVE TENSOR TO DEVICE
# ==============================

matrix_on_device = matrix.to(device)

print("Matrix device:", matrix_on_device.device)


# ==============================
# 9. NEURAL NETWORK LAYER MATH
# ==============================

inputs = torch.rand(32, 4)

weights = torch.rand(4, 6)

bias = torch.rand(6)

z = inputs @ weights + bias

print("Inputs shape:", inputs.shape)
print("Weights shape:", weights.shape)
print("Bias shape:", bias.shape)
print("Output shape:", z.shape)



import torch

x1 = torch.tensor(1.0)
x2 = torch.tensor(2.0)

w1 = torch.tensor(0.5, requires_grad=True)
w2 = torch.tensor(-0.3, requires_grad=True)
bias = torch.tensor(0.1, requires_grad=True)

z = (x1 * w1) + (x2 * w2) + bias

print("Forward result:", z.item())

z.backward()

print("Gradient of w1:", w1.grad.item())
print("Gradient of w2:", w2.grad.item())
print("Gradient of bias:", bias.grad.item())








import torch

# Parameters
w1 = torch.tensor(0.5, requires_grad=True)
w2 = torch.tensor(-0.3, requires_grad=True)
bias = torch.tensor(0.1, requires_grad=True)

# Inputs
x1 = torch.tensor(1.0)
x2 = torch.tensor(2.0)

# Forward pass
z = (x1 * w1) + (x2 * w2) + bias

# Backpropagation
z.backward()

# Gradients
print("w1 gradient:", w1.grad)
print("w2 gradient:", w2.grad)
print("bias gradient:", bias.grad)








optimizer.zero_grad()

predictions = model(inputs)

loss = loss_function(predictions, targets)

loss.backward()

optimizer.step()









import torch
import torch.nn as nn

class TinyModel(nn.Module):

    def __init__(self):
        super().__init__()

        self.hidden = nn.Linear(2, 4)
        self.output = nn.Linear(4, 1)

        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.hidden(x)
        x = self.relu(x)
        x = self.output(x)

        return x
    
    
    
    
for epoch in range(200):

    optimizer.zero_grad()

    predictions = model(inputs)

    loss = loss_function(predictions, targets)

    loss.backward()

    optimizer.step()
    
    
    






import torch
import torch.nn as nn
import torch.optim as optim


class TinyModel(nn.Module):

    def __init__(self):
        super().__init__()

        self.hidden = nn.Linear(2, 4)
        self.output = nn.Linear(4, 1)

        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.hidden(x)
        x = self.relu(x)
        x = self.output(x)

        return x


inputs = torch.tensor([
    [0., 0.],
    [0., 1.],
    [1., 0.],
    [1., 1.]
])

targets = torch.tensor([
    [0.],
    [0.],
    [0.],
    [1.]
])


model = TinyModel()

loss_function = nn.BCEWithLogitsLoss()

optimizer = optim.SGD(
    model.parameters(),
    lr=0.1
)


for epoch in range(200):

    optimizer.zero_grad()

    predictions = model(inputs)

    loss = loss_function(
        predictions,
        targets
    )

    loss.backward()

    optimizer.step()

    if epoch % 50 == 0:
        print(
            f"Epoch {epoch}, "
            f"Loss: {loss.item():.4f}"
        )
        
        
        
        
        
        
        
        
        
        
import torch
import torch.nn as nn
import torch.optim as optim


class MyModel(nn.Module):

    def __init__(self, input_features, hidden_features, output_features):
        super().__init__()

        self.layer1 = nn.Linear(
            input_features,
            hidden_features
        )

        self.relu = nn.ReLU()

        self.layer2 = nn.Linear(
            hidden_features,
            output_features
        )

    def forward(self, x):

        x = self.layer1(x)

        x = self.relu(x)

        x = self.layer2(x)

        return x


inputs = torch.tensor([
    [0., 0.],
    [0., 1.],
    [1., 0.],
    [1., 1.]
])

targets = torch.tensor([
    [0.],
    [0.],
    [0.],
    [1.]
])


model = MyModel(
    input_features=2,
    hidden_features=4,
    output_features=1
)


loss_function = nn.BCEWithLogitsLoss()


optimizer = optim.SGD(
    model.parameters(),
    lr=0.1
)


epochs = 200

model.train()

for epoch in range(epochs):

    optimizer.zero_grad()

    predictions = model(inputs)

    loss = loss_function(
        predictions,
        targets
    )

    loss.backward()

    optimizer.step()

    if epoch % 50 == 0:
        print(
            f"Epoch {epoch}: "
            f"Loss = {loss.item():.4f}"
        )


model.eval()

with torch.no_grad():

    predictions = model(inputs)

    probabilities = torch.sigmoid(predictions)

    print("\nPredictions:")

    print(probabilities)
    
    
    
    
    
    
    
    
import torch
from torch.utils.data import Dataset


class AndGateDataset(Dataset):

    def __init__(self):

        self.inputs = torch.tensor([
            [0., 0.],
            [0., 1.],
            [1., 0.],
            [1., 1.]
        ])

        self.targets = torch.tensor([
            [0.],
            [0.],
            [0.],
            [1.]
        ])

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, index):
        return self.inputs[index], self.targets[index]
    
    
    
    
    
    
    
def __getitem__(self, index):

    image_path = self.paths[index]

    image = load_image(image_path)

    image = resize(image)

    image = normalize(image)

    label = self.labels[index]

    return image, label










import torch
from torch.utils.data import Dataset, DataLoader


class AndGateDataset(Dataset):

    def __init__(self):

        self.inputs = torch.tensor([
            [0., 0.],
            [0., 1.],
            [1., 0.],
            [1., 1.]
        ])

        self.targets = torch.tensor([
            [0.],
            [0.],
            [0.],
            [1.]
        ])

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, index):
        return self.inputs[index], self.targets[index]


dataset = AndGateDataset()

loader = DataLoader(
    dataset,
    batch_size=2,
    shuffle=True
)


for batch_index, (batch_inputs, batch_targets) in enumerate(loader):

    print("Batch:", batch_index)

    print("Inputs:")
    print(batch_inputs)

    print("Targets:")
    print(batch_targets)

    print("Input shape:", batch_inputs.shape)
    print("Target shape:", batch_targets.shape)
    
    
    
    
    
    
    
    
    
    
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader


class AndGateDataset(Dataset):

    def __init__(self):

        self.inputs = torch.tensor([
            [0., 0.],
            [0., 1.],
            [1., 0.],
            [1., 1.]
        ])

        self.targets = torch.tensor([
            [0.],
            [0.],
            [0.],
            [1.]
        ])

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, index):
        return self.inputs[index], self.targets[index]


class TinyModel(nn.Module):

    def __init__(self):
        super().__init__()

        self.hidden = nn.Linear(2, 4)
        self.relu = nn.ReLU()
        self.output = nn.Linear(4, 1)

    def forward(self, x):

        x = self.hidden(x)

        x = self.relu(x)

        x = self.output(x)

        return x


dataset = AndGateDataset()

loader = DataLoader(
    dataset,
    batch_size=2,
    shuffle=True
)


model = TinyModel()

loss_function = nn.BCEWithLogitsLoss()

optimizer = optim.SGD(
    model.parameters(),
    lr=0.5
)


epochs = 300

model.train()

for epoch in range(epochs):

    epoch_loss = 0.0

    for batch_inputs, batch_targets in loader:

        optimizer.zero_grad()

        predictions = model(batch_inputs)

        loss = loss_function(
            predictions,
            batch_targets
        )

        loss.backward()

        optimizer.step()

        epoch_loss += loss.item()

    if epoch % 100 == 0 or epoch == epochs - 1:

        print(
            f"Epoch {epoch}: "
            f"Loss = {epoch_loss:.4f}"
        )
        
        
        
        
        
    
    
    
    
    
    
import torch
from torch.utils.data import Dataset, DataLoader


class MyDataset(Dataset):

    def __init__(self, inputs, targets):

        self.inputs = inputs
        self.targets = targets

    def __len__(self):

        return len(self.inputs)

    def __getitem__(self, index):

        return (
            self.inputs[index],
            self.targets[index]
        )


inputs = torch.tensor([
    [0., 0.],
    [0., 1.],
    [1., 0.],
    [1., 1.]
])

targets = torch.tensor([
    [0.],
    [0.],
    [0.],
    [1.]
])


dataset = MyDataset(
    inputs,
    targets
)


loader = DataLoader(
    dataset,
    batch_size=2,
    shuffle=True
)


for batch_inputs, batch_targets in loader:

    print("Input shape:", batch_inputs.shape)

    print("Target shape:", batch_targets.shape)
    
    
    
    
    
    







import torch
import torch.nn as nn


class TinyModel(nn.Module):

    def __init__(self):
        super().__init__()

        self.hidden = nn.Linear(2, 4)
        self.output = nn.Linear(4, 1)
        self.relu = nn.ReLU()

    def forward(self, x):

        x = self.hidden(x)

        x = self.relu(x)

        x = self.output(x)

        return x


model = TinyModel()

torch.save(
    model.state_dict(),
    "tiny_model.pth"
)

print("Model saved.")


loaded_model = TinyModel()

saved_state = torch.load(
    "tiny_model.pth"
)

loaded_model.load_state_dict(
    saved_state
)

loaded_model.eval()

print("Model loaded.")











loaded_model = TinyModel()

loaded_optimizer = optim.SGD(
    loaded_model.parameters(),
    lr=0.1
)

loaded_checkpoint = torch.load(
    "tiny_model_checkpoint.pt"
)

loaded_model.load_state_dict(
    loaded_checkpoint["model_state_dict"]
)

loaded_optimizer.load_state_dict(
    loaded_checkpoint["optimizer_state_dict"]
)

resumed_epoch = loaded_checkpoint["epoch"]

print("Resumed from epoch:", resumed_epoch)












import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader


class AndGateDataset(Dataset):

    def __init__(self):

        self.inputs = torch.tensor([
            [0., 0.],
            [0., 1.],
            [1., 0.],
            [1., 1.]
        ])

        self.targets = torch.tensor([
            [0.],
            [0.],
            [0.],
            [1.]
        ])

    def __len__(self):

        return len(self.inputs)

    def __getitem__(self, index):

        return (
            self.inputs[index],
            self.targets[index]
        )


class TinyModel(nn.Module):

    def __init__(self):

        super().__init__()

        self.hidden = nn.Linear(2, 4)

        self.relu = nn.ReLU()

        self.output = nn.Linear(4, 1)

    def forward(self, x):

        x = self.hidden(x)

        x = self.relu(x)

        x = self.output(x)

        return x


dataset = AndGateDataset()

loader = DataLoader(
    dataset,
    batch_size=2,
    shuffle=True
)


model = TinyModel()

loss_function = nn.BCEWithLogitsLoss()

optimizer = optim.SGD(
    model.parameters(),
    lr=0.5
)


epochs = 300


model.train()

for epoch in range(epochs):

    epoch_loss = 0.0

    for batch_inputs, batch_targets in loader:

        optimizer.zero_grad()

        predictions = model(batch_inputs)

        loss = loss_function(
            predictions,
            batch_targets
        )

        loss.backward()

        optimizer.step()

        epoch_loss += loss.item()

    if epoch % 100 == 0 or epoch == epochs - 1:

        print(
            f"Epoch {epoch}: "
            f"Loss = {epoch_loss:.4f}"
        )


checkpoint = {
    "epoch": epochs,
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict()
}


torch.save(
    checkpoint,
    "and_gate_checkpoint.pt"
)

print("Checkpoint saved.")


loaded_model = TinyModel()

loaded_optimizer = optim.SGD(
    loaded_model.parameters(),
    lr=0.5
)


loaded_checkpoint = torch.load(
    "and_gate_checkpoint.pt"
)


loaded_model.load_state_dict(
    loaded_checkpoint["model_state_dict"]
)

loaded_optimizer.load_state_dict(
    loaded_checkpoint["optimizer_state_dict"]
)


loaded_model.eval()

sample_input = torch.tensor([
    [1., 1.]
])


with torch.no_grad():

    prediction = loaded_model(
        sample_input
    )

    probability = torch.sigmoid(
        prediction
    )

print(
    "Prediction:",
    probability.item()
)
    
    
    
    
    
    
    
import torch
import torch.nn as nn
from torchvision import models

weights = models.ResNet18_Weights.DEFAULT
model = models.resnet18(weights=weights)

for parameter in model.parameters():
    parameter.requires_grad = False

model.fc = nn.Linear(model.fc.in_features, 4)

for parameter in model.fc.parameters():
    parameter.requires_grad = True
    
    
    
    
    
    
    
    
    
    

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, datasets
from torch.utils.data import DataLoader

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

weights = models.ResNet18_Weights.DEFAULT
preprocess = weights.transforms()

train_dataset = datasets.ImageFolder(
    "data/train",
    transform=preprocess
)

val_dataset = datasets.ImageFolder(
    "data/val",
    transform=preprocess
)

if train_dataset.classes != val_dataset.classes:
    raise ValueError("Training and validation classes do not match.")

num_classes = len(train_dataset.classes)

train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=32,
    shuffle=False
)

model = models.resnet18(weights=weights)

for parameter in model.parameters():
    parameter.requires_grad = False

model.fc = nn.Linear(
    model.fc.in_features,
    num_classes
)

for parameter in model.fc.parameters():
    parameter.requires_grad = True

model = model.to(device)

loss_function = nn.CrossEntropyLoss()

optimizer = optim.Adam(
    model.fc.parameters(),
    lr=0.001
)

best_val_accuracy = 0.0
epochs = 5

for epoch in range(epochs):
    model.train()
    train_loss = 0.0

    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        logits = model(images)

        loss = loss_function(logits, labels)

        loss.backward()
        optimizer.step()

        train_loss += loss.item()

    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(device)
            labels = labels.to(device)

            logits = model(images)
            predictions = logits.argmax(dim=1)

            correct += (predictions == labels).sum().item()
            total += labels.size(0)

    val_accuracy = correct / total if total > 0 else 0.0

    print(
        f"Epoch {epoch + 1}/{epochs} | "
        f"Train loss: {train_loss:.4f} | "
        f"Validation accuracy: {val_accuracy:.2%}"
    )

    if val_accuracy > best_val_accuracy:
        best_val_accuracy = val_accuracy

        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "class_names": train_dataset.classes,
                "validation_accuracy": val_accuracy
            },
            "best_transfer_model.pt"
        )

print("Best validation accuracy:", f"{best_val_accuracy:.2%}")











import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models

weights = models.ResNet18_Weights.DEFAULT
model = models.resnet18(weights=weights)

num_classes = 4
model.fc = nn.Linear(model.fc.in_features, num_classes)

for parameter in model.parameters():
    parameter.requires_grad = False

for parameter in model.layer4.parameters():
    parameter.requires_grad = True

for parameter in model.fc.parameters():
    parameter.requires_grad = True

optimizer = optim.SGD(
    [
        {"params": model.layer4.parameters(), "lr": 0.0001},
        {"params": model.fc.parameters(), "lr": 0.01}
    ],
    momentum=0.9
)

loss_function = nn.CrossEntropyLoss()

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)
model = model.to(device)

for epoch in range(5):
    model.train()

    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        logits = model(images)
        loss = loss_function(logits, labels)
        loss.backward()
        optimizer.step()

    model.eval()
    validation_loss = 0.0
    validation_count = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(device)
            labels = labels.to(device)

            logits = model(images)
            loss = loss_function(logits, labels)

            validation_loss += loss.item() * labels.size(0)
            validation_count += labels.size(0)

    mean_val_loss = (
        validation_loss / validation_count
        if validation_count > 0 else float("nan")
    )

    print(
        f"Epoch {epoch + 1}: "
        f"Validation loss = {mean_val_loss:.4f}"
    )
    
    
    
    
    
    
    
    
    
    
import pandas as pd
import torch
import torch.nn as nn

class TinyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.Linear(2, 4)
        self.output = nn.Linear(4, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.hidden(x))
        return self.output(x)

model = TinyModel()
model.eval()

def score_batch(df):
    inputs = torch.tensor(
        df[["x1", "x2"]].values,
        dtype=torch.float32
    )

    with torch.no_grad():
        logits = model(inputs)
        probabilities = torch.sigmoid(logits).squeeze(1)

    return pd.Series(probabilities.tolist(), index=df.index)

batch = pd.DataFrame({
    "x1": [0.0, 0.0, 1.0, 1.0],
    "x2": [0.0, 1.0, 0.0, 1.0]
})

batch["predicted_probability"] = score_batch(batch)

print(batch)












import pandas as pd
import torch
import torch.nn as nn

from pyspark.sql import functions as F
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import DoubleType


class TinyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.Linear(2, 4)
        self.output = nn.Linear(4, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.hidden(x))
        return self.output(x)


def load_model():
    model = TinyModel()

    state = torch.load(
        "tiny_model.pth",
        map_location="cpu",
        weights_only=True
    )

    model.load_state_dict(state)
    model.eval()

    return model


model = load_model()


@pandas_udf(DoubleType())
def score_batch(x1: pd.Series, x2: pd.Series) -> pd.Series:
    inputs = torch.tensor(
        pd.concat([x1, x2], axis=1).values,
        dtype=torch.float32
    )

    with torch.no_grad():
        logits = model(inputs)
        probabilities = torch.sigmoid(logits).squeeze(1)

    return pd.Series(probabilities.tolist())


scored_df = input_df.withColumn(
    "predicted_probability",
    score_batch(F.col("x1"), F.col("x2"))
)








import torch
import torch.nn as nn
import torch.optim as optim

torch.manual_seed(42)

X = torch.tensor([
    [50.0, 1.0, 20.0],
    [80.0, 2.0, 15.0],
    [100.0, 2.0, 10.0],
    [120.0, 3.0, 8.0],
    [150.0, 3.0, 5.0],
    [180.0, 4.0, 2.0]
])

y = torch.tensor([
    [20.0],
    [32.0],
    [40.0],
    [48.0],
    [60.0],
    [72.0]
])

class HousePriceModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(3, 8),
            nn.ReLU(),
            nn.Linear(8, 1)
        )

    def forward(self, x):
        return self.network(x)

model = HousePriceModel()

loss_function = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

for epoch in range(500):
    model.train()

    predictions = model(X)
    loss = loss_function(predictions, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

torch.save(model.state_dict(), "house_model.pth")

loaded_model = HousePriceModel()
loaded_model.load_state_dict(
    torch.load("house_model.pth", map_location="cpu", weights_only=True)
)
loaded_model.eval()

new_house = torch.tensor([[130.0, 3.0, 6.0]])

with torch.no_grad():
    predicted_price = loaded_model(new_house)

print("Predicted house price:", predicted_price.item())













Inference: use learned weights to make predictions.
Batch inference: score many already-available records together; optimize throughput.
Real-time serving: respond quickly to individual live requests; optimize latency.
PyTorch inference pattern
model.eval()with torch.no_grad():    outputs = model(inputs)



Batch scoring function
def score_batch(df):    inputs = torch.tensor(        df[["x1", "x2"]].values,        dtype=torch.float32    )    with torch.no_grad():        outputs = model(inputs)    return outputs



Spark UDF choices
- Standard UDF: row-oriented function execution.
- Pandas UDF: vectorized batches of values.
- Spark distributes partitions; vectorization improves per-batch scoring efficiency.
Remember: load the model once per worker process and reuse it. Preserve the training feature order and preprocessing.













import torch

def load_model(model, checkpoint_path, device="cpu"):
    model = model.to(device)

    state_dict = torch.load(
        checkpoint_path,
        map_location=device,
        weights_only=True
    )

    model.load_state_dict(state_dict)
    model.eval()

    return model


def predict(model, input_tensor, device="cpu"):
    model.eval()
    input_tensor = input_tensor.to(device)

    with torch.no_grad():
        output = model(input_tensor)

    return output


# Example usage:
# model = HousePriceModel()
# model = load_model(model, "house_model.pth")
# sample = torch.tensor([[130.0, 3.0, 6.0]])
# result = predict(model, sample)
# print(result.item())




import torch
import torch.nn as nn

# 1. Define the model architecture
class TinyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.Linear(2, 4)
        self.relu = nn.ReLU()
        self.output = nn.Linear(4, 1)

    def forward(self, x):
        x = self.relu(self.hidden(x))
        return self.output(x)


# 2. Create the model and switch to inference mode
model = TinyModel()
model.eval()

# 3. Create an example input: one row, two features
example_input = torch.rand(1, 2)

# 4. Convert with tracing
traced_model = torch.jit.trace(model, example_input)
traced_model.save("tiny_model_traced.pt")

# 5. Convert with scripting
scripted_model = torch.jit.script(model)
scripted_model.save("tiny_model_scripted.pt")

# 6. Load the scripted model back
loaded_model = torch.jit.load("tiny_model_scripted.pt")
loaded_model.eval()

# 7. Make a prediction
sample = torch.tensor([[1.0, 1.0]])

with torch.no_grad():
    original_output = model(sample)
    loaded_output = loaded_model(sample)

print("Original model output:", original_output.item())
print("Loaded model output:", loaded_output.item())

# 8. Compare both outputs
print(
    "Outputs match:",
    torch.allclose(original_output, loaded_output, atol=1e-6)
)









# Save the model's learned parameters
torch.save(model.state_dict(), "tiny_model_weights.pth")

# Load the saved parameters
model_again = TinyModel()

weights = torch.load(
    "tiny_model_weights.pth",
    map_location="cpu",
    weights_only=True
)

model_again.load_state_dict(weights)
model_again.eval()









import torch
import torch.nn as nn

# Define the SAME architecture used during training
class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(2, 8),
            nn.ReLU(),
            nn.Linear(8, 1)
        )

    def forward(self, x):
        return self.network(x)


# SAVE — run after training
model = MyModel()
# ... train model here ...
torch.save(model.state_dict(), "model.pth")


# LOAD — in your inference application
device = torch.device("cpu")

loaded_model = MyModel()
state_dict = torch.load(
    "model.pth",
    map_location=device,
    weights_only=True
)
loaded_model.load_state_dict(state_dict)
loaded_model.eval()

# PREDICT
sample = torch.tensor([[1.0, 2.0]], dtype=torch.float32)

with torch.no_grad():
    prediction = loaded_model(sample)

print(prediction)










import pandas as pd
import torch
import torch.nn as nn


# 1. Define a model that accepts two input features
class TinyModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.hidden = nn.Linear(2, 4)
        self.relu = nn.ReLU()
        self.output = nn.Linear(4, 1)

    def forward(self, x):
        x = self.relu(self.hidden(x))
        return self.output(x)


# 2. Create a model and put it in evaluation mode
model = TinyModel()
model.eval()


# 3. Define a function that scores an entire batch
def score_batch(df: pd.DataFrame) -> pd.Series:
    # Extract features in the exact order expected by the model
    inputs = torch.tensor(
        df[["x1", "x2"]].values,
        dtype=torch.float32
    )

    # Inference: no gradient calculation is needed
    with torch.no_grad():
        raw_outputs = model(inputs)

        # Convert logits into values between 0 and 1
        probabilities = torch.sigmoid(raw_outputs).squeeze(1)

    # Return one prediction for each input row
    return pd.Series(probabilities.tolist(), index=df.index)


# 4. Create a sample batch of four records
batch = pd.DataFrame({
    "x1": [0.0, 0.0, 1.0, 1.0],
    "x2": [0.0, 1.0, 0.0, 1.0]
})


# 5. Score all four rows in one model call
batch["predicted_probability"] = score_batch(batch)


# 6. Display the predictions
print(batch)











import pandas as pd
import torch

from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import DoubleType


# Assumes model is already loaded and in evaluation mode.
@pandas_udf(DoubleType())
def predict_batch(x1: pd.Series, x2: pd.Series) -> pd.Series:
    inputs = torch.tensor(
        pd.concat([x1, x2], axis=1).values,
        dtype=torch.float32
    )

    with torch.no_grad():
        raw_outputs = model(inputs)
        probabilities = torch.sigmoid(raw_outputs).squeeze(1)

    return pd.Series(probabilities.tolist())


# Example Spark DataFrame: spark_df contains x1 and x2 columns.
scored_df = spark_df.withColumn(
    "predicted_probability",
    predict_batch(spark_df["x1"], spark_df["x2"])
)









import random
import torch

# Both models use the same architecture.
model_v1 = HousePriceModel()
model_v2 = HousePriceModel()

model_v1.load_state_dict(
    torch.load("house_model_v1.pth",
               map_location="cpu",
               weights_only=True)
)

model_v2.load_state_dict(
    torch.load("house_model_v2.pth",
               map_location="cpu",
               weights_only=True)
)

model_v1.eval()
model_v2.eval()

# Route approximately 10% of requests to Version 2.
NEW_MODEL_PERCENT = 10


def choose_model():
    random_number = random.random() * 100

    if random_number < NEW_MODEL_PERCENT:
        return "v2", model_v2

    return "v1", model_v1


def predict_with_version(input_tensor):
    version, model = choose_model()

    with torch.no_grad():
        prediction = model(input_tensor)

    # In production, send this to structured application logs.
    print(f"Model version used: {version}")

    return {
        "model_version": version,
        "prediction": prediction.tolist()
    }





