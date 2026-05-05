import numpy as np
import pandas as pd
import os
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression

class CourseScorePredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False
        self.accuracy_score = 0.0
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'dataset.csv')
        self._train_model()

    def _train_model(self):
        # Set up MLflow experiment
        mlflow.set_experiment("Course_Score_Prediction")
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)

        # 1. Generate or Load Data (for DVC tracking)
        n_samples = 200
        if not os.path.exists(self.data_path):
            np.random.seed(42)
            hours = np.random.uniform(0, 20, n_samples)
            prev_scores = np.random.uniform(40, 100, n_samples)
            difficulties = np.random.choice([-5.0, -2.5, 0.0, 2.5], n_samples)
            
            y = 10.0 + (5.0 * hours) + (0.6 * prev_scores) + difficulties + np.random.normal(0, 2.0, n_samples)
            y = np.clip(y, 0, 100)
            
            df = pd.DataFrame({
                'hours_studied': hours,
                'previous_score': prev_scores,
                'difficulty_modifier': difficulties,
                'target_score': y
            })
            df.to_csv(self.data_path, index=False)
            print("Generated new synthetic dataset for DVC tracking.")
        
        # Load dataset
        df = pd.read_csv(self.data_path)
        X = df[['hours_studied', 'previous_score', 'difficulty_modifier']].values
        y = df['target_score'].values

        # 2. Train and Track with MLflow
        with mlflow.start_run():
            # Log parameters
            mlflow.log_param("n_samples", len(df))
            mlflow.log_param("model_type", "LinearRegression")
            
            # Train the model
            self.model.fit(X, y)
            
            # Evaluate and log metrics
            self.accuracy_score = self.model.score(X, y)
            mlflow.log_metric("r2_score", self.accuracy_score)
            
            # Log the model artifacts
            mlflow.sklearn.log_model(self.model, "linear_regression_model")
            
            self.is_trained = True

    def predict(self, course_name: str, hours_studied: float, previous_score: float) -> float:
        # Determine difficulty based on course name
        difficulty_modifier = 0.0
        if "Quantum" in course_name:
            difficulty_modifier = -5.0
        elif "Deep Learning" in course_name or "Advanced" in course_name:
            difficulty_modifier = -2.5
        elif "Agile" in course_name or "Foundations" in course_name:
            difficulty_modifier = +2.5

        # Format input for the model
        X_new = np.array([[hours_studied, previous_score, difficulty_modifier]])
        
        # Use Scikit-Learn .predict()
        prediction = self.model.predict(X_new)[0]
        return round(min(max(prediction, 0), 100.0), 2)

# Instantiate singleton to train once on server startup
predictor_instance = CourseScorePredictor()

def predict_score(course_name: str, hours_studied: float, previous_score: float) -> float:
    return predictor_instance.predict(course_name, hours_studied, previous_score)

def get_model_score() -> float:
    """Returns the R^2 score of the trained ML model"""
    return predictor_instance.accuracy_score
