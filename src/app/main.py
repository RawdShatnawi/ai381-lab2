"""FastAPI service for the churn model."""
import os
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

MODEL_VERSION = "1.0.0"
MODEL_PATH = os.environ.get("MODEL_PATH", "models/model.joblib")

model = joblib.load(MODEL_PATH)
app = FastAPI(title="AI381 Churn API", version=MODEL_VERSION)

NUMERIC = ["tenure_months", "monthly_charges", "support_calls"]
CATEGORICAL = ["contract", "internet_service"]


class Customer(BaseModel):
    tenure_months: int = Field(ge=0)
    monthly_charges: float = Field(gt=0)
    contract: str
    internet_service: str
    support_calls: int = Field(ge=0)


@app.get("/health")
def health():
    return {"status": "ok", "model_version": MODEL_VERSION}


@app.post("/predict")
def predict(c: Customer):
    X = pd.DataFrame([c.model_dump()])[NUMERIC + CATEGORICAL]
    p = float(model.predict_proba(X)[0, 1])
    return {"churn_probability": round(p, 3), "model_version": MODEL_VERSION}
