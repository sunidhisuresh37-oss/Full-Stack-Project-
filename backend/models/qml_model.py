import math
try:
    import pennylane as qml
    from pennylane import numpy as np
    
    # Define a simple 1-qubit quantum circuit for binary classification
    dev = qml.device("default.qubit", wires=1)

    @qml.qnode(dev)
    def circuit(feature1, feature2):
        # Embed features into the quantum state
        qml.RX(feature1, wires=0)
        qml.RY(feature2, wires=0)
        # Measure expectation value in Z basis
        return qml.expval(qml.PauliZ(0))

    def quantum_classify(course_name: str, feature1: float, feature2: float) -> str:
        # Get expectation value [-1, 1]
        exp_val = circuit(feature1, feature2)
        
        # Adjust classification threshold based on course difficulty
        threshold = 0.0
        if "Quantum" in course_name:
            threshold = 0.2 # Harder to classify as High Engagement

        if exp_val > threshold:
            return "Class A: High Engagement Pattern"
        else:
            return "Class B: Low Engagement Pattern"
            
except ImportError:
    # Fallback if pennylane is not installed
    def quantum_classify(course_name: str, feature1: float, feature2: float) -> str:
        # Mocking the quantum interference pattern using simple math
        val = math.cos(feature1) * math.sin(feature2)
        
        threshold = 0.0
        if "Quantum" in course_name:
            threshold = 0.2

        if val > threshold:
            return "Class A: High Engagement Pattern (Simulated QML)"
        else:
            return "Class B: Low Engagement Pattern (Simulated QML)"
