import numpy as np
import pandas as pd

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


RANDOM_STATE = 42


def main():
    iris = load_iris()

    X = iris.data
    y = iris.target

    hyperparameters = {
        "n_estimators": 100,
        "random_state": RANDOM_STATE,
    }

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model = RandomForestClassifier(**hyperparameters)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Точность accuracy: {accuracy:.2f}")


if __name__ == "__main__":
    main()
