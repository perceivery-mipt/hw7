import os
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")
RANDOM_STATE = 42


def get_n_estimators(model_version: str) -> int:
    if model_version == "v1.1.0":
        return 100
    return 50


def train_model():
    iris = load_iris()

    X = iris.data
    y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=get_n_estimators(MODEL_VERSION),
        random_state=RANDOM_STATE,
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return model, iris.target_names.tolist(), accuracy


model, target_names, accuracy = train_model()

app = FastAPI(
    title="HW7 Iris ML Service",
    description="ML service based on the Iris RandomForest pipeline",
    version=MODEL_VERSION,
)


class PredictRequest(BaseModel):
    features: List[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="Four Iris features: sepal length, sepal width, petal length, petal width",
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": MODEL_VERSION,
        "model": "RandomForestClassifier",
        "n_estimators": get_n_estimators(MODEL_VERSION),
    }


@app.get("/metrics")
def metrics():
    return {
        "version": MODEL_VERSION,
        "accuracy": round(float(accuracy), 4),
    }


@app.post("/predict")
def predict(request: PredictRequest):
    prediction = int(model.predict([request.features])[0])

    return {
        "version": MODEL_VERSION,
        "predicted_class": prediction,
        "predicted_name": target_names[prediction],
    }
