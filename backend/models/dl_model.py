# Simulated Deep Learning sentiment analysis
# For demonstration purposes, we avoid loading heavy PyTorch/Transformers models
# but structure the code as if it does.
# import torch
# from transformers import pipeline

def analyze_sentiment(course_name: str, feedback: str) -> str:
    positive_words = {"good", "great", "excellent", "awesome", "understand", "clear", "amazing", "love", "best", "perfect"}
    negative_words = {"bad", "poor", "confusing", "hard", "difficult", "unclear", "terrible", "worst", "hate", "boring"}
    negations = {"not", "no", "never", "none", "don't", "dont", "doesn't", "doesnt", "isn't", "isnt", "wasn't", "wasnt"}
    
    words = feedback.lower().replace(".", " ").replace(",", " ").replace("!", " ").split()
    
    score = 0
    is_negated = False
    
    for word in words:
        if word in negations:
            is_negated = True
            continue
            
        if word in positive_words:
            score += -1 if is_negated else 1
            is_negated = False
        elif word in negative_words:
            score += 1 if is_negated else -1
            is_negated = False
            
    if score > 0:
        return "POSITIVE"
    elif score < 0:
        return "NEGATIVE"
    else:
        return "NEUTRAL"
