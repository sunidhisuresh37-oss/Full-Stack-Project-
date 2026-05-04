import numpy as np
from sklearn.linear_model import LinearRegression

# A simple simulated model for demonstration
# In a real scenario, this would load a pre-trained model using joblib or pickle
def predict_score(course_name: str, hours_studied: float, previous_score: float) -> float:
    # Adjust prediction difficulty based on the course
    difficulty_modifier = 0.0
    if "Quantum" in course_name:
        difficulty_modifier = -5.0 # Quantum is harder!
    elif "Deep Learning" in course_name or "Advanced" in course_name:
        difficulty_modifier = -2.5
    elif "Agile" in course_name or "Foundations" in course_name:
        difficulty_modifier = +2.5

    predicted_score = 10.0 + (5.0 * hours_studied) + (0.6 * previous_score) + difficulty_modifier
    return round(min(max(predicted_score, 0), 100.0), 2)
