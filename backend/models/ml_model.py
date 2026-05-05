import numpy as np
from sklearn.linear_model import LinearRegression

class CourseScorePredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False
        self.accuracy_score = 0.0
        self._train_model()

    def _train_model(self):
        # Generate synthetic data for training
        np.random.seed(42)
        # Features: [hours_studied, previous_score, difficulty_modifier]
        n_samples = 200
        hours = np.random.uniform(0, 20, n_samples)
        prev_scores = np.random.uniform(40, 100, n_samples)
        difficulties = np.random.choice([-5.0, -2.5, 0.0, 2.5], n_samples)
        
        X = np.column_stack((hours, prev_scores, difficulties))
        # Underlying real function + some noise to make it realistic
        y = 10.0 + (5.0 * hours) + (0.6 * prev_scores) + difficulties + np.random.normal(0, 2.0, n_samples)
        y = np.clip(y, 0, 100) # Ensure scores are between 0 and 100
        
        # Actually train the model using Scikit-Learn .fit()
        self.model.fit(X, y)
        
        # Calculate and store the model's R-squared score using .score()
        self.accuracy_score = self.model.score(X, y)
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
