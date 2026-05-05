from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from models import ml_model, dl_model, qml_model, rnn_model
import database

app = FastAPI(title="E-Learning Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# New Models for Database-Driven API
class CourseRequest(BaseModel):
    course_name: str
    student_id: int = 1 # Defaulting to 1 for prototype

class TextData(BaseModel):
    course_name: str
    feedback: str
    student_id: int = 1

class RNNTipRequest(BaseModel):
    course_name: str
    score: float

@app.get("/")
def read_root():
    return {"message": "Welcome to E-Learning Analytics API"}

@app.get("/dashboard")
def get_dashboard(student_id: int = 1):
    # Dynamically fetch course progress from the SQLite Database
    data = database.get_dashboard_data(student_id)
    return {"courses": data}

@app.post("/predict/ml")
def predict_ml(data: CourseRequest):
    # 1. Automatically fetch the hidden student stats from the Database!
    stats = database.get_course_stats(data.student_id, data.course_name)
    if not stats:
        raise HTTPException(status_code=404, detail="Course data not found in DB")
    
    # 2. Feed those DB stats into the Machine Learning Model
    prediction = ml_model.predict_score(data.course_name, stats["hours_studied"], stats["previous_score"])
    
    return {
        "model": "Machine Learning", 
        "predicted_score": prediction,
        "data_used_from_db": {"hours_studied": stats["hours_studied"], "previous_score": stats["previous_score"]}
    }

@app.post("/predict/dl")
def predict_dl(data: TextData):
    # Sentiment analysis still requires manual text input (the feedback)
    sentiment = dl_model.analyze_sentiment(data.course_name, data.feedback)
    return {"model": "Deep Learning", "sentiment": sentiment}

@app.post("/predict/qml")
def predict_qml(data: CourseRequest):
    # 1. Automatically fetch hidden engagement metrics from the Database!
    stats = database.get_course_stats(data.student_id, data.course_name)
    if not stats:
        raise HTTPException(status_code=404, detail="Course data not found in DB")

    # 2. Feed those DB stats into the Quantum Machine Learning Circuit
    classification = qml_model.quantum_classify(data.course_name, stats["login_frequency"], stats["video_completion_rate"])
    
    return {
        "model": "Quantum Machine Learning", 
        "classification_result": classification,
        "data_used_from_db": {"login_frequency": stats["login_frequency"], "video_completion_rate": stats["video_completion_rate"]}
    }

@app.post("/predict/rnn_tips")
def predict_rnn_tips(data: RNNTipRequest):
    tips = rnn_model.generate_study_tips(data.course_name, data.score)
    return {"model": "RNN (NumPy)", "tips": tips}
