import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from feature_engineering import FeatureEngineering


class ModelTrainer:

    def __init__(self):
        self.dataset_path = "repository_features.csv"
        self.model_path = "growth_model.pkl"

    # --------------------------------------------------
    # Load Dataset
    # --------------------------------------------------
    def load_dataset(self):

        if os.path.exists(self.dataset_path):
            return pd.read_csv(self.dataset_path)

        print("Dataset not found. Creating dataset...")

        fe = FeatureEngineering()
        df = fe.save_dataset(self.dataset_path)
        fe.close()

        return df

    # --------------------------------------------------
    # Train Growth Model
    # --------------------------------------------------
    def train_growth_model(self):

        df = self.load_dataset()

        if len(df) < 5:
            raise ValueError(
                "Not enough repositories to train a model."
            )

        # Features
        X = df[
            [
                "stars",
                "forks",
                "watchers",
                "contributors",
                "commits",
                "issues",
                "closed_issues",
                "pull_requests",
                "merged_prs",
                "releases",
                "merge_rate",
                "community_engagement",
            ]
        ]

        # Target
        y = df["health_score"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
        )

        model = RandomForestRegressor(
            n_estimators=200,
            random_state=42,
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        joblib.dump(model, self.model_path)

        print("=" * 50)
        print("Growth Model Trained Successfully")
        print("=" * 50)
        print(f"MAE : {mae:.3f}")
        print(f"MSE : {mse:.3f}")
        print(f"R²  : {r2:.3f}")
        print("=" * 50)
        print(f"Model saved to {self.model_path}")

        return model


if __name__ == "__main__":

    trainer = ModelTrainer()
    trainer.train_growth_model()