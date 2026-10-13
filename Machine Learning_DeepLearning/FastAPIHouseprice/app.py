
from contextlib import asynccontextmanager

import torch
import torch.nn as nn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


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


class HouseRequest(BaseModel):
    area: float = Field(gt=0)
    bedrooms: int = Field(ge=1, le=20)
    age: float = Field(ge=0)


class HouseResponse(BaseModel):
    predicted_price: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    device = torch.device("cpu")

    model = HousePriceModel()
    state_dict = torch.load(
        "house_model.pth",
        map_location=device,
        weights_only=True
    )

    model.load_state_dict(state_dict)
    model.eval()

    app.state.model = model
    app.state.device = device

    yield


app = FastAPI(
    title="House Price Prediction API",
    lifespan=lifespan
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=HouseResponse)
def predict(request: HouseRequest):
    model = app.state.model
    device = app.state.device

    input_tensor = torch.tensor(
        [[request.area, request.bedrooms, request.age]],
        dtype=torch.float32,
        device=device
    )

    with torch.no_grad():
        prediction = model(input_tensor)

    return HouseResponse(
        predicted_price=float(prediction.item())
    )
