
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
