"""
================================================================================
DEEP LEARNING & MODEL SERVING REFERENCE IMPLEMENTATIONS & CODE COOKBOOK
================================================================================
A structured, end-to-end boilerplate and reference guide covering:
  1. Neuron Foundations from Scratch (Pure Python & NumPy)
  2. Multi-Layer Perceptron (MLP) Forward Pass & Matrix Transformations
  3. Loss Functions from Scratch (MSE & Binary Cross-Entropy)
  4. Backpropagation & Manual Gradient Descent on Logic Gates (AND/OR Gate)
  5. PyTorch Tensors: Creation, Shapes, Reshaping, Dtypes & GPU Acceleration
  6. PyTorch Autograd: Computation Graphs, Dynamic Derivatives & Gradients
  7. PyTorch Neural Network Building Blocks (nn.Module, nn.Linear, nn.Sequential)
  8. Canonical PyTorch 5-Step Training Loop & Evaluation (model.train / model.eval)
  9. Custom Datasets & DataLoaders (Batching, Shuffling, Transforms)
 10. Model Checkpointing: Saving & Resuming Training (State Dicts)
 11. Transfer Learning Suite: Feature Extraction vs. Fine-Tuning (ResNet18)
 12. Transfer Learning: Differential Learning Rates across Parameter Groups
 13. Model Serving: Production-Ready FastAPI REST Endpoint with Pydantic Validation
 14. Model Serialization: TorchScript Compilation (Tracing vs. Scripting)
 15. High-Throughput Batch Inference (Vectorized Scoring & Pandas UDF Pattern)
 16. Production Deployment: Canary Routing, A/B Testing & Automated Rollback
================================================================================
"""

# ==============================================================================
# 1. NEURON FOUNDATIONS FROM SCRATCH (PURE PYTHON & NUMPY)
# ==============================================================================
print("\n" + "=" * 80)
print("1. NEURON FOUNDATIONS FROM SCRATCH (PURE PYTHON & NUMPY)")
print("=" * 80)

import math
import numpy as np

# ------------------------------------------------------------------------------
# 1.1 Single Neuron in Pure Python (Pre-Activation Weighted Sum)
# ------------------------------------------------------------------------------
def single_neuron_raw(inputs, weights, bias):
    """
    Computes raw linear weighted sum z = sum(x_i * w_i) + b.
    Inputs and weights must have identical length.
    """
    if len(inputs) != len(weights):
        raise ValueError(f"Shape mismatch: {len(inputs)} inputs vs {len(weights)} weights")
    
    weighted_sum = sum(x * w for x, w in zip(inputs, weights))
    z = weighted_sum + bias
    return z

sample_inputs = [1.0, 2.0]
sample_weights = [0.5, -0.3]
sample_bias = 0.1

z_raw = single_neuron_raw(sample_inputs, sample_weights, sample_bias)
print(f"Single Neuron Raw Weighted Sum z: {z_raw:.4f}")  # Expect 0.0


# ------------------------------------------------------------------------------
# 1.2 Single Neuron with Non-Linear Activations (Sigmoid & ReLU)
# ------------------------------------------------------------------------------
def sigmoid_scalar(z):
    """Sigmoid activation: squashes any real value into probability range (0, 1)."""
    return 1.0 / (1.0 + math.exp(-z))

def relu_scalar(z):
    """ReLU activation: returns z if positive, else returns 0."""
    return max(0.0, z)

def single_neuron_activated(inputs, weights, bias, activation_fn=relu_scalar):
    """Computes weighted sum and applies non-linear activation a = f(z)."""
    z = single_neuron_raw(inputs, weights, bias)
    a = activation_fn(z)
    return z, a

z_val, a_sigmoid = single_neuron_activated(sample_inputs, sample_weights, sample_bias, sigmoid_scalar)
_, a_relu = single_neuron_activated(sample_inputs, sample_weights, sample_bias, relu_scalar)

print(f"Neuron with Sigmoid Output a: {a_sigmoid:.4f}")
print(f"Neuron with ReLU Output a:    {a_relu:.4f}")


# ------------------------------------------------------------------------------
# 1.3 Vectorized Single Neuron in NumPy
# ------------------------------------------------------------------------------
def numpy_neuron(x, w, b, activation="relu"):
    """
    Vectorized neuron computation: z = w^T * x + b using numpy dot product.
    """
    z = np.dot(w, x) + b
    if activation == "relu":
        a = np.maximum(0, z)
    elif activation == "sigmoid":
        a = 1.0 / (1.0 + np.exp(-z))
    else:
        a = z
    return z, a

x_vec = np.array([2.0, 3.0, 4.0])
w_vec = np.array([0.5, 1.0, -0.2])
b_val = 0.5

z_np, a_np = numpy_neuron(x_vec, w_vec, b_val, activation="relu")
print(f"NumPy Vectorized Neuron -> z: {z_np:.4f}, activated: {a_np:.4f}")


# ==============================================================================
# 2. MULTI-LAYER PERCEPTRON (MLP) FORWARD PASS & MATRIX TRANSFORMATIONS
# ==============================================================================
print("\n" + "=" * 80)
print("2. MULTI-LAYER PERCEPTRON (MLP) FORWARD PASS & MATRIX TRANSFORMATIONS")
print("=" * 80)

# ------------------------------------------------------------------------------
# 2.1 Layer-Level Matrix Transformation: Z = X @ W + b
# ------------------------------------------------------------------------------
# Batch of 2 samples, each with 3 input features
X_batch = np.array([
    [2.0, 3.0, 4.0],
    [1.0, 5.0, 2.0]
])  # Shape: (2, 3)

# Weight matrix for a layer with 2 neurons (each takes 3 inputs)
W_layer1 = np.array([
    [0.5, 0.2],
    [1.0, -0.4],
    [-0.2, 0.7]
])  # Shape: (3, 2)

# Bias vector for 2 neurons
b_layer1 = np.array([0.5, -0.1])  # Shape: (2,)

# Forward linear transformation
Z_layer1 = X_batch @ W_layer1 + b_layer1  # Shape: (2, 2)
A_layer1 = np.maximum(0, Z_layer1)         # Apply ReLU activation

print("Layer 1 Pre-activation Matrix Z (Shape 2x2):")
print(Z_layer1)
print("Layer 1 Activated Output Matrix A (Shape 2x2):")
print(A_layer1)


# ------------------------------------------------------------------------------
# 2.2 Deep Multi-Layer Feedforward Network (Hand-Traced Forward Pass)
# ------------------------------------------------------------------------------
class SimpleNumPyMLP:
    """
    3-Layer Multi-Layer Perceptron implemented completely in NumPy:
    Architecture: Input(2) -> Hidden1(3) -> Hidden2(2) -> Output(1)
    """
    def __init__(self):
        # Layer 1: 2 inputs -> 3 hidden neurons
        self.W1 = np.array([[0.5, 0.2, 0.1], [0.4, 0.8, 0.3]])
        self.b1 = np.array([0.1, 0.2, 0.1])

        # Layer 2: 3 inputs -> 2 hidden neurons
        self.W2 = np.array([[0.3, 0.5], [0.7, 0.2], [0.4, 0.6]])
        self.b2 = np.array([0.1, 0.2])

        # Output Layer: 2 inputs -> 1 output neuron
        self.W3 = np.array([[0.5], [0.8]])
        self.b3 = np.array([0.1])

    def forward(self, X):
        # Layer 1
        self.Z1 = X @ self.W1 + self.b1
        self.A1 = np.maximum(0, self.Z1)  # ReLU

        # Layer 2
        self.Z2 = self.A1 @ self.W2 + self.b2
        self.A2 = np.maximum(0, self.Z2)  # ReLU

        # Output Layer (Regression: linear output)
        self.Z3 = self.A2 @ self.W3 + self.b3
        self.output = self.Z3
        return self.output

mlp = SimpleNumPyMLP()
sample_input = np.array([[2.0, 3.0]])
prediction_mlp = mlp.forward(sample_input)
print(f"NumPy 3-Layer MLP Prediction for input [2.0, 3.0]: {prediction_mlp[0, 0]:.4f}")


# ==============================================================================
# 3. LOSS FUNCTIONS FROM SCRATCH (MSE & BINARY CROSS-ENTROPY)
# ==============================================================================
print("\n" + "=" * 80)
print("3. LOSS FUNCTIONS FROM SCRATCH (MSE & BINARY CROSS-ENTROPY)")
print("=" * 80)

# ------------------------------------------------------------------------------
# 3.1 Mean Squared Error (MSE) for Regression
# ------------------------------------------------------------------------------
def compute_mse_loss(y_true, y_pred):
    """Computes MSE: (1/n) * sum((y_true - y_pred)^2)."""
    n = len(y_true)
    squared_errors = [(yt - yp) ** 2 for yt, yp in zip(y_true, y_pred)]
    return sum(squared_errors) / n

true_prices = [50.0, 65.0, 40.0]
pred_prices = [48.0, 70.0, 44.0]
mse_result = compute_mse_loss(true_prices, pred_prices)
print(f"Mean Squared Error (MSE): {mse_result:.4f}")


# ------------------------------------------------------------------------------
# 3.2 Binary Cross-Entropy (BCE) Loss for Classification
# ------------------------------------------------------------------------------
def compute_bce_loss(y_true, y_pred_prob, epsilon=1e-12):
    """
    Computes Binary Cross-Entropy Loss: -[y*log(p) + (1-y)*log(1-p)].
    Uses epsilon clipping to prevent numerical instability at log(0).
    """
    clipped_p = min(max(y_pred_prob, epsilon), 1.0 - epsilon)
    loss = - (y_true * math.log(clipped_p) + (1.0 - y_true) * math.log(1.0 - clipped_p))
    return loss

loss_confident_correct = compute_bce_loss(y_true=1, y_pred_prob=0.95)
loss_confident_wrong   = compute_bce_loss(y_true=1, y_pred_prob=0.05)

print(f"BCE Loss (Confident Correct, p=0.95): {loss_confident_correct:.4f}")
print(f"BCE Loss (Confident Wrong,   p=0.05): {loss_confident_wrong:.4f} (Heavily penalized)")


# ==============================================================================
# 4. BACKPROPAGATION & MANUAL GRADIENT DESCENT ON LOGIC GATES (AND GATE)
# ==============================================================================
print("\n" + "=" * 80)
print("4. BACKPROPAGATION & MANUAL GRADIENT DESCENT (TRAINING A SINGLE NEURON)")
print("=" * 80)

import random

# Complete from-scratch training of a single sigmoid neuron to learn the logical AND gate
# Truth table: (0,0)->0, (0,1)->0, (1,0)->0, (1,1)->1
and_gate_data = [
    ([0.0, 0.0], 0.0),
    ([0.0, 1.0], 0.0),
    ([1.0, 0.0], 0.0),
    ([1.0, 1.0], 1.0)
]

# Initialize weights and bias randomly
random.seed(42)
w1 = random.uniform(-0.5, 0.5)
w2 = random.uniform(-0.5, 0.5)
bias = random.uniform(-0.5, 0.5)
learning_rate = 0.5
epochs = 600

print(f"Initial Random Parameters -> w1: {w1:.3f}, w2: {w2:.3f}, bias: {bias:.3f}")

for epoch in range(epochs):
    epoch_loss = 0.0
    for (x1, x2), y_true in and_gate_data:
        # 1. Forward Pass
        z = (x1 * w1) + (x2 * w2) + bias
        p = 1.0 / (1.0 + math.exp(-z))  # Sigmoid

        # 2. Loss Computation
        loss = compute_bce_loss(y_true, p)
        epoch_loss += loss

        # 3. Backpropagation (Chain Rule for Sigmoid + BCE loss simplifies to: dL/dz = p - y)
        dloss_dz = p - y_true
        grad_w1 = dloss_dz * x1
        grad_w2 = dloss_dz * x2
        grad_bias = dloss_dz * 1.0

        # 4. Gradient Descent Parameter Updates
        w1 -= learning_rate * grad_w1
        w2 -= learning_rate * grad_w2
        bias -= learning_rate * grad_bias

    if epoch % 200 == 0 or epoch == epochs - 1:
        print(f"Epoch {epoch:>3} | Average BCE Loss: {epoch_loss / len(and_gate_data):.4f}")

print("\nFinal Trained AND Gate Predictions:")
for (x1, x2), y_true in and_gate_data:
    z = (x1 * w1) + (x2 * w2) + bias
    pred = 1.0 / (1.0 + math.exp(-z))
    print(f"  Inputs: ({x1}, {x2}) | Target: {y_true} | Predicted: {pred:.4f} -> Class: {1 if pred > 0.5 else 0}")


# ==============================================================================
# 5. PYTORCH TENSORS: CREATION, SHAPES, RESHAPING, DTYPES & GPU ACCELERATION
# ==============================================================================
print("\n" + "=" * 80)
print("5. PYTORCH TENSORS: CREATION, SHAPES, RESHAPING, DTYPES & GPU")
print("=" * 80)

import torch

# ------------------------------------------------------------------------------
# 5.1 Device Configuration
# ------------------------------------------------------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Active Compute Device: {device}")

# ------------------------------------------------------------------------------
# 5.2 Tensor Creation & Dimensionality
# ------------------------------------------------------------------------------
scalar_t = torch.tensor(7.0)                     # 0-D tensor: shape ()
vector_t = torch.tensor([1.0, 2.0, 3.0])         # 1-D tensor: shape (3,)
matrix_t = torch.tensor([[1.0, 2.0], [3.0, 4.0]])# 2-D tensor: shape (2, 2)
zeros_t  = torch.zeros(2, 3)                     # Shape: (2, 3)
ones_t   = torch.ones(2, 3)                      # Shape: (2, 3)
rand_t   = torch.rand(2, 3)                      # Uniform random in [0, 1)
arange_t = torch.arange(0, 10)                   # [0, 1, ..., 9]

print(f"Vector Tensor: {vector_t} | Shape: {vector_t.shape} | Dtype: {vector_t.dtype}")
print(f"Matrix Tensor Shape: {matrix_t.shape} | Device: {matrix_t.device}")

# ------------------------------------------------------------------------------
# 5.3 Reshaping, Views & Matrix Operations
# ------------------------------------------------------------------------------
flat_t = ones_t.reshape(6)  # Reshape from (2, 3) to (6,)
print(f"Reshaped Tensor Shape: {flat_t.shape}")

# Element-wise operations vs Matrix Multiplication
a_mat = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
b_mat = torch.tensor([[5.0, 6.0], [7.0, 8.0]])

elem_mult = a_mat * b_mat  # [[1*5, 2*6], [3*7, 4*8]] = [[5, 12], [21, 32]]
matmul_res = a_mat @ b_mat # Row-by-column matrix multiplication

print("Element-wise Multiplication (a * b):")
print(elem_mult)
print("Matrix Multiplication (a @ b):")
print(matmul_res)

# Simulated Layer Linear Transformation in PyTorch
inputs_batch = torch.rand(32, 4)   # 32 samples, 4 features
weights_layer = torch.rand(4, 6)   # 4 input features, 6 output neurons
bias_layer = torch.rand(6)         # 6 biases

layer_output = inputs_batch @ weights_layer + bias_layer
print(f"Batched Layer Output Shape: {layer_output.shape}")  # Expect (32, 6)


# ==============================================================================
# 6. PYTORCH AUTOGRAD: COMPUTATION GRAPHS & DYNAMIC DERIVATIVES
# ==============================================================================
print("\n" + "=" * 80)
print("6. PYTORCH AUTOGRAD: COMPUTATION GRAPHS & DYNAMIC DERIVATIVES")
print("=" * 80)

# Set up trainable parameters with requires_grad=True
w1_t = torch.tensor(0.5, requires_grad=True)
w2_t = torch.tensor(-0.3, requires_grad=True)
b_t  = torch.tensor(0.1, requires_grad=True)

# Non-trainable input features
x1_t = torch.tensor(1.0)
x2_t = torch.tensor(2.0)

# 1. Forward Pass (Autograd records operations in dynamic computation graph)
z_t = (x1_t * w1_t) + (x2_t * w2_t) + b_t
print(f"Autograd Forward z output: {z_t.item():.4f}")

# 2. Backward Pass (Triggers automatic chain rule differentiation)
z_t.backward()

# 3. Read accumulated partial derivatives from .grad attributes
print("Autograd Computed Gradients:")
print(f"  dz / dw1:  {w1_t.grad.item():.4f} (Expected: x1 = 1.0)")
print(f"  dz / dw2:  {w2_t.grad.item():.4f} (Expected: x2 = 2.0)")
print(f"  dz / db:   {b_t.grad.item():.4f}  (Expected: 1.0)")

# Disabling Gradients for Evaluation/Serving via torch.no_grad()
with torch.no_grad():
    inference_z = (x1_t * w1_t) + (x2_t * w2_t) + b_t
    print(f"Inference with torch.no_grad(): {inference_z.item():.4f} (No graph recorded)")


# ==============================================================================
# 7. PYTORCH NEURAL NETWORK BUILDING BLOCKS (TORCH.NN.MODULE)
# ==============================================================================
print("\n" + "=" * 80)
print("7. PYTORCH NEURAL NETWORK BUILDING BLOCKS (TORCH.NN.MODULE)")
print("=" * 80)

import torch.nn as nn

class ConfigurableMLP(nn.Module):
    """
    Production-style configurable Multi-Layer Perceptron built with PyTorch.
    Demonstrates nn.Linear, activations, and parameter tracking.
    """
    def __init__(self, in_features, hidden_features, out_features, dropout_prob=0.1):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(in_features, hidden_features),
            nn.ReLU(),
            nn.Dropout(p=dropout_prob),
            nn.Linear(hidden_features, hidden_features),
            nn.ReLU(),
            nn.Linear(hidden_features, out_features)
        )

    def forward(self, x):
        return self.network(x)

mlp_model = ConfigurableMLP(in_features=4, hidden_features=16, out_features=1)
print("ConfigurableMLP Architecture:")
print(mlp_model)

total_trainable_params = sum(p.numel() for p in mlp_model.parameters() if p.requires_grad)
print(f"Total Trainable Parameters: {total_trainable_params}")


# ==============================================================================
# 8. CANONICAL PYTORCH 5-STEP TRAINING LOOP & EVALUATION
# ==============================================================================
print("\n" + "=" * 80)
print("8. CANONICAL PYTORCH 5-STEP TRAINING LOOP & EVALUATION")
print("=" * 80)

import torch.optim as optim

# Synthetic training data for AND gate
X_train_t = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]], dtype=torch.float32)
y_train_t = torch.tensor([[0.], [0.], [0.], [1.]], dtype=torch.float32)

class TinyClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.Linear(2, 4)
        self.relu = nn.ReLU()
        self.output = nn.Linear(4, 1)

    def forward(self, x):
        return self.output(self.relu(self.hidden(x)))

torch.manual_seed(42)
classifier_model = TinyClassifier()

# Loss: BCEWithLogitsLoss combines Sigmoid + BCE with mathematical stability
loss_fn = nn.BCEWithLogitsLoss()
optimizer = optim.SGD(classifier_model.parameters(), lr=0.5)

print("Starting 5-Step PyTorch Training Loop (200 Epochs)...")
classifier_model.train()

for epoch in range(200):
    # Step 1: Clear old accumulated gradients
    optimizer.zero_grad()

    # Step 2: Forward pass (compute model logits)
    predictions = classifier_model(X_train_t)

    # Step 3: Compute scalar loss
    loss = loss_fn(predictions, y_train_t)

    # Step 4: Backward pass (compute gradients via Autograd)
    loss.backward()

    # Step 5: Optimizer step (nudge weights downhill)
    optimizer.step()

    if (epoch + 1) % 50 == 0:
        print(f"  Epoch [{epoch+1:>3}/200] | Loss: {loss.item():.4f}")

# Evaluation Mode with torch.no_grad()
classifier_model.eval()
with torch.no_grad():
    raw_logits = classifier_model(X_train_t)
    probs = torch.sigmoid(raw_logits)
    binary_preds = (probs > 0.5).int()

print("\nFinal Evaluated Predictions:")
for i in range(len(X_train_t)):
    inputs = X_train_t[i].tolist()
    target = int(y_train_t[i].item())
    prob = probs[i].item()
    pred_cls = binary_preds[i].item()
    print(f"  Input: {inputs} | Target: {target} | Prob: {prob:.4f} | Predicted: {pred_cls}")


# ==============================================================================
# 9. CUSTOM DATASETS & DATALOADERS (BATCHING, SHUFFLING, TRANSFORMS)
# ==============================================================================
print("\n" + "=" * 80)
print("9. CUSTOM DATASETS & DATALOADERS (BATCHING, SHUFFLING, TRANSFORMS)")
print("=" * 80)

from torch.utils.data import Dataset, DataLoader

class LogicGateDataset(Dataset):
    """
    Custom PyTorch Dataset implementing the 3 mandatory methods:
      __init__: Loads data, precomputes indices, stores optional transforms
      __len__:  Returns total observation count
      __getitem__: Fetches a single index, applies transforms, returns tensors
    """
    def __init__(self, data_pairs, transform=None):
        self.data_pairs = data_pairs
        self.transform = transform

    def __len__(self):
        return len(self.data_pairs)

    def __getitem__(self, idx):
        features, target = self.data_pairs[idx]
        x_tensor = torch.tensor(features, dtype=torch.float32)
        y_tensor = torch.tensor([target], dtype=torch.float32)

        if self.transform:
            x_tensor = self.transform(x_tensor)

        return x_tensor, y_tensor

# On-the-fly feature scaling transform function
def add_slight_jitter(tensor):
    return tensor + torch.randn_like(tensor) * 0.01

logic_dataset = LogicGateDataset(
    data_pairs=[
        ([0.0, 0.0], 0.0),
        ([0.0, 1.0], 0.0),
        ([1.0, 0.0], 0.0),
        ([1.0, 1.0], 1.0)
    ],
    transform=add_slight_jitter
)

# DataLoader handles batching, shuffling, and multi-process loading
batch_loader = DataLoader(
    dataset=logic_dataset,
    batch_size=2,
    shuffle=True,
    drop_last=False
)

print(f"Dataset Total Samples: {len(logic_dataset)}")
print(f"Number of Batches per Epoch (batch_size=2): {len(batch_loader)}")

for batch_idx, (batch_x, batch_y) in enumerate(batch_loader):
    print(f"  Batch {batch_idx + 1}: x shape={batch_x.shape}, y shape={batch_y.shape}")


# ==============================================================================
# 10. MODEL CHECKPOINTING: SAVING & RESUMING TRAINING (STATE DICTS)
# ==============================================================================
print("\n" + "=" * 80)
print("10. MODEL CHECKPOINTING: SAVING & RESUMING TRAINING (STATE DICTS)")
print("=" * 80)

checkpoint_filepath = "model_training_checkpoint.pt"

# Step 1: Save Comprehensive Checkpoint (weights + optimizer moments + epoch)
checkpoint_payload = {
    "epoch": 100,
    "model_state_dict": classifier_model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "best_val_loss": 0.0421
}

torch.save(checkpoint_payload, checkpoint_filepath)
print(f"Successfully serialized full checkpoint to '{checkpoint_filepath}'.")

# Step 2: Freshly Instantiate Architecture and Restore from Checkpoint
resumed_model = TinyClassifier()
resumed_optimizer = optim.SGD(resumed_model.parameters(), lr=0.5)

loaded_checkpoint = torch.load(checkpoint_filepath, map_location="cpu", weights_only=True)
resumed_model.load_state_dict(loaded_checkpoint["model_state_dict"])
resumed_optimizer.load_state_dict(loaded_checkpoint["optimizer_state_dict"])
resumed_epoch = loaded_checkpoint["epoch"]

print(f"Resumed Model Successfully from Saved Epoch: {resumed_epoch}")

# Step 3: Run Inference with Restored Model in Evaluation Mode
resumed_model.eval()
with torch.no_grad():
    test_input = torch.tensor([[1.0, 1.0]], dtype=torch.float32)
    test_output = torch.sigmoid(resumed_model(test_input))
    print(f"Restored Model Prediction for [1.0, 1.0]: {test_output.item():.4f}")


# ==============================================================================
# 11. TRANSFER LEARNING SUITE: FEATURE EXTRACTION VS. FINE-TUNING (RESNET18)
# ==============================================================================
print("\n" + "=" * 80)
print("11. TRANSFER LEARNING SUITE: FEATURE EXTRACTION VS. FINE-TUNING")
print("=" * 80)

try:
    from torchvision import models

    # --------------------------------------------------------------------------
    # Strategy A: Feature Extraction (Freeze Backbone, Train New Final Layer)
    # --------------------------------------------------------------------------
    # Initialize ResNet18 with pretrained ImageNet weights
    weights = models.ResNet18_Weights.DEFAULT
    resnet_extractor = models.resnet18(weights=weights)

    # Freeze every parameter in the pretrained convolutional backbone
    for param in resnet_extractor.parameters():
        param.requires_grad = False

    # Replace the 1,000-class ImageNet fully connected head with a 4-class head
    num_target_classes = 4
    resnet_extractor.fc = nn.Linear(resnet_extractor.fc.in_features, num_target_classes)
    # Note: newly assigned layers automatically have requires_grad=True by default

    # Verify parameter counts
    trainable_p = sum(p.numel() for p in resnet_extractor.parameters() if p.requires_grad)
    frozen_p    = sum(p.numel() for p in resnet_extractor.parameters() if not p.requires_grad)

    print("--- Strategy A: Feature Extraction (ResNet18) ---")
    print(f"  Trainable Parameters (Head only): {trainable_p:>8,}")
    print(f"  Frozen Parameters (Backbone):     {frozen_p:>8,}")
    print(f"  Expected Transforms: {weights.transforms()}")

except Exception as e:
    print(f"[NOTE] torchvision models download skipped or offline: {e}")
    print("Standard Feature Extraction Code Pattern demonstrated below:")
    print("""
    from torchvision import models
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    for param in model.parameters():
        param.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    """)


# ==============================================================================
# 12. TRANSFER LEARNING: DIFFERENTIAL LEARNING RATES PER PARAMETER GROUP
# ==============================================================================
print("\n" + "=" * 80)
print("12. DIFFERENTIAL LEARNING RATES PER PARAMETER GROUP (FINE-TUNING)")
print("=" * 80)

# Simulate fine-tuning architecture with a backbone and a classification head
class CustomFineTuneModel(nn.Module):
    def __init__(self, in_features=128, num_classes=3):
        super().__init__()
        # Simulated pretrained backbone
        self.backbone_layer1 = nn.Linear(in_features, 64)
        self.backbone_layer2 = nn.Linear(64, 32)
        # Newly added task-specific classification head
        self.fc_head = nn.Linear(32, num_classes)

    def forward(self, x):
        x = torch.relu(self.backbone_layer1(x))
        x = torch.relu(self.backbone_layer2(x))
        return self.fc_head(x)

ft_model = CustomFineTuneModel()

# Unfreeze backbone layer 2 and the head, keep layer 1 frozen
for param in ft_model.backbone_layer1.parameters():
    param.requires_grad = False
for param in ft_model.backbone_layer2.parameters():
    param.requires_grad = True

# Assign Differential Learning Rates via Parameter Groups:
#   - Backbone gets a gentle learning rate (1e-4) to prevent catastrophic forgetting
#   - Newly added head gets a large learning rate (1e-2) to learn the new task rapidly
differential_optimizer = optim.Adam([
    {"params": ft_model.backbone_layer2.parameters(), "lr": 1e-4},
    {"params": ft_model.fc_head.parameters(),         "lr": 1e-2}
], weight_decay=1e-4)

print("Configured Differential Parameter Groups:")
for group_idx, group in enumerate(differential_optimizer.param_groups):
    param_count = sum(p.numel() for p in group["params"])
    print(f"  Group {group_idx}: {param_count} parameters | Configured Learning Rate: {group['lr']}")


# ==============================================================================
# 13. MODEL SERVING: PRODUCTION-READY FASTAPI ENDPOINT WITH PYDANTIC VALIDATION
# ==============================================================================
print("\n" + "=" * 80)
print("13. PRODUCTION MODEL SERVING: FASTAPI & PYDANTIC VALIDATION")
print("=" * 80)

try:
    import os
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field
    from contextlib import asynccontextmanager

    # 1. Pydantic Request Model with Strict Boundary Constraints
    class PredictionRequest(BaseModel):
        x1: float = Field(..., ge=0.0, le=1.0, description="Feature 1 in range [0, 1]")
        x2: float = Field(..., ge=0.0, le=1.0, description="Feature 2 in range [0, 1]")

    # 2. Pydantic Response Model
    class PredictionResponse(BaseModel):
        predicted_probability: float
        predicted_class: int
        model_version: str

    # 3. Lifespan Context Manager: Loads model ONCE at startup, NOT per request!
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup: Load model once into memory
        loaded = TinyClassifier()
        if os.path.exists(checkpoint_filepath):
            state = torch.load(checkpoint_filepath, map_location="cpu", weights_only=True)
            loaded.load_state_dict(state["model_state_dict"])
        loaded.eval()
        app.state.model = loaded
        print("[FastAPI Startup] Model loaded once into application state.")
        yield
        # Shutdown: Resource cleanup
        app.state.model = None
        print("[FastAPI Shutdown] Model state released.")

    app = FastAPI(title="Logic Gate Serving Endpoint", version="1.0.0", lifespan=lifespan)

    @app.get("/health")
    def health_check():
        """Standard liveness probe for load balancers and Kubernetes."""
        return {"status": "healthy", "service": "logic-gate-inference"}

    @app.post("/predict", response_model=PredictionResponse)
    def predict_endpoint(request: PredictionRequest):
        """Production inference route with strict Pydantic validation."""
        model = getattr(app.state, "model", None)
        if model is None:
            raise HTTPException(status_code=503, detail="Model service not initialized")

        input_tensor = torch.tensor([[request.x1, request.x2]], dtype=torch.float32)

        with torch.no_grad():
            raw_logits = model(input_tensor)
            prob = torch.sigmoid(raw_logits).item()
            cls_pred = 1 if prob >= 0.5 else 0

        return PredictionResponse(
            predicted_probability=round(prob, 4),
            predicted_class=cls_pred,
            model_version="v1.0"
        )

    print("FastAPI Application & Pydantic Validation Pipeline Configured Successfully.")

except ImportError:
    print("[NOTE] 'fastapi' or 'pydantic' not installed. Production code blueprint shown above.")


# ==============================================================================
# 14. MODEL SERIALIZATION: TORCHSCRIPT COMPILATION (TRACING VS. SCRIPTING)
# ==============================================================================
print("\n" + "=" * 80)
print("14. MODEL SERIALIZATION: TORCHSCRIPT (TRACING VS. SCRIPTING)")
print("=" * 80)

# Compile PyTorch model into TorchScript for deployment in C++ runtime environments
dummy_input = torch.rand(1, 2)
classifier_model.eval()

# Method A: Tracing (Records operations for fixed computation flow)
traced_model = torch.jit.trace(classifier_model, dummy_input)
traced_model_path = "model_compiled_traced.pt"
traced_model.save(traced_model_path)

# Method B: Scripting (Parses Python AST directly to capture dynamic conditionals)
scripted_model = torch.jit.script(classifier_model)
scripted_model_path = "model_compiled_scripted.pt"
scripted_model.save(scripted_model_path)

# Load compiled model back WITHOUT requiring Python class definition
loaded_jit = torch.jit.load(scripted_model_path)
loaded_jit.eval()

with torch.no_grad():
    sample_tensor = torch.tensor([[1.0, 1.0]], dtype=torch.float32)
    orig_res = classifier_model(sample_tensor)
    jit_res  = loaded_jit(sample_tensor)
    match_check = torch.allclose(orig_res, jit_res, atol=1e-6)

print(f"Traced Model Saved to:   '{traced_model_path}'")
print(f"Scripted Model Saved to: '{scripted_model_path}'")
print(f"TorchScript and Original Python Outputs Match Identically: {match_check}")


# ==============================================================================
# 15. HIGH-THROUGHPUT BATCH INFERENCE (VECTORIZED SCORING & PANDAS UDF)
# ==============================================================================
print("\n" + "=" * 80)
print("15. HIGH-THROUGHPUT BATCH INFERENCE (VECTORIZED SCORING & PANDAS UDF)")
print("=" * 80)

import pandas as pd

# Simulate batch of 1,000 incoming customer records
np.random.seed(42)
batch_df = pd.DataFrame({
    "x1": np.random.uniform(0.0, 1.0, size=1000),
    "x2": np.random.uniform(0.0, 1.0, size=1000)
})

def vectorized_score_batch(df: pd.DataFrame, model_to_use) -> pd.Series:
    """
    Scores an entire batch of thousands of records in a SINGLE model forward pass,
    mirroring the exact execution architecture of a PySpark Pandas UDF.
    """
    # 1. Convert entire DataFrame partition to a single 2-D float32 tensor
    inputs_tensor = torch.tensor(df[["x1", "x2"]].values, dtype=torch.float32)

    # 2. Execute inference without tracking gradients
    with torch.no_grad():
        logits = model_to_use(inputs_tensor)
        probabilities = torch.sigmoid(logits).squeeze(1).numpy()

    # 3. Return series aligned with DataFrame index
    return pd.Series(probabilities, index=df.index)

batch_df["predicted_probability"] = vectorized_score_batch(batch_df, classifier_model)
batch_df["predicted_class"] = (batch_df["predicted_probability"] >= 0.5).astype(int)

print(f"Batch Scoring Complete on {len(batch_df):,} records:")
print(batch_df.head(5).to_string())


# ==============================================================================
# 16. PRODUCTION DEPLOYMENT: CANARY ROUTING, A/B TESTING & AUTOMATED ROLLBACK
# ==============================================================================
print("\n" + "=" * 80)
print("16. PRODUCTION DEPLOYMENT: CANARY ROUTING & AUTOMATED ROLLBACK")
print("=" * 80)

class CanaryDeploymentRouter:
    """
    Production traffic router that directs a controlled percentage of requests
    to a candidate canary model (v2) while routing primary traffic to stable model (v1).
    Monitors error rate and triggers automated rollback if errors exceed threshold.
    """
    def __init__(self, model_v1, model_v2, canary_percentage=10, max_error_threshold=0.05):
        self.model_v1 = model_v1
        self.model_v2 = model_v2
        self.canary_percentage = canary_percentage  # e.g., 10%
        self.max_error_threshold = max_error_threshold
        self.v1_requests = 0
        self.v2_requests = 0
        self.v2_errors = 0
        self.rollback_triggered = False

    def route_and_predict(self, input_tensor):
        if self.rollback_triggered:
            # Automatic Rollback Active: 100% traffic goes strictly to stable Model v1
            self.v1_requests += 1
            with torch.no_grad():
                return "v1_stable (ROLLED_BACK)", self.model_v1(input_tensor)

        # Decide routing based on configured canary traffic percentage
        is_canary = (random.randint(1, 100) <= self.canary_percentage)
        selected_version = "v2_canary" if is_canary else "v1_stable"

        try:
            if is_canary:
                self.v2_requests += 1
                with torch.no_grad():
                    output = self.model_v2(input_tensor)
            else:
                self.v1_requests += 1
                with torch.no_grad():
                    output = self.model_v1(input_tensor)
            return selected_version, output

        except Exception as e:
            if is_canary:
                self.v2_errors += 1
                # Check for automated rollback condition
                canary_error_rate = self.v2_errors / max(1, self.v2_requests)
                if canary_error_rate > self.max_error_threshold:
                    self.rollback_triggered = True
                    print(f"\n[ALERT] Canary error rate exceeded {self.max_error_threshold:.1%}. TRIGGERING AUTOMATED ROLLBACK TO V1!")
            raise e

# Instantiate stable v1 and experimental v2
model_stable_v1 = TinyClassifier()
model_canary_v2 = TinyClassifier()
router = CanaryDeploymentRouter(model_stable_v1, model_canary_v2, canary_percentage=15)

print("Simulating 100 Live Production Requests Through Canary Router (15% Traffic to Canary)...")
for _ in range(100):
    sample = torch.rand(1, 2)
    version_used, _ = router.route_and_predict(sample)

print("\nCanary Deployment Traffic Summary:")
print(f"  Stable Model v1 Requests Handled: {router.v1_requests:>3} ({router.v1_requests}% of total)")
print(f"  Canary Model v2 Requests Handled: {router.v2_requests:>3} ({router.v2_requests}% of total)")
print(f"  Canary Rollback Status:           {'TRIGGERED' if router.rollback_triggered else 'HEALTHY'}")

print("\n" + "=" * 80)
print("DEEP LEARNING & MODEL SERVING MODULES (SECTIONS 1 TO 16) COMPLETED SUCCESSFULLY")
print("=" * 80)
