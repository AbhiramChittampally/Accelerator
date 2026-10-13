
import torch
import torch.nn as nn
import torch.optim as optim

torch.manual_seed(42)

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

X = torch.tensor([
    [50., 1., 20.],
    [80., 2., 15.],
    [100., 2., 10.],
    [120., 3., 8.],
    [150., 3., 5.],
    [180., 4., 2.]
])

y = torch.tensor([
    [20.], [32.], [40.],
    [48.], [60.], [72.]
])

model = HousePriceModel()
loss_fn = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

for epoch in range(500):
    predictions = model(X)
    loss = loss_fn(predictions, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

torch.save(model.state_dict(), "house_model.pth")

print("Created house_model.pth")
