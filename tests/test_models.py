import unittest
import sys
import os

# Add backend directory to sys.path so we can import models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from models import ml_model

class TestMLModel(unittest.TestCase):
    def test_ml_model_prediction(self):
        # Test that the model successfully initializes, trains, and predicts
        score = ml_model.predict_score("Test Course", 10.0, 80.0)
        self.assertTrue(0 <= score <= 100)
        
    def test_ml_model_score(self):
        # Check that the model trained correctly and has a positive R^2 score
        score = ml_model.get_model_score()
        self.assertTrue(score > 0.0)

if __name__ == '__main__':
    unittest.main()
