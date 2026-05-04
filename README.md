# E-Learning Platform with Test Analytics

This is a full-stack project built following Agile methodologies. It features a modern web frontend and a Python FastAPI backend that serves predictive endpoints using Machine Learning (ML), Deep Learning (DL), and Quantum Machine Learning (QML).

## Project Structure
- `/backend`: Contains the FastAPI application and Python model code.
- `/frontend`: Contains the vanilla HTML/CSS/JS frontend (no Node.js setup required, open directly in browser).
- `/docs`: Contains Agile methodology, SRS, and Test Plan documents.

## How to Run

### 1. Start the Backend
Open a terminal in the `backend` folder and run the following:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```
The backend API will run on `http://localhost:8000`.

### 2. Open the Frontend
Since the frontend uses standard web technologies, simply open the `frontend/index.html` file in your preferred web browser. Alternatively, use a tool like Live Server.

You can now interact with the ML, DL, and QML services directly from the User Interface!
