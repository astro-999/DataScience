from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os

app = FastAPI(title="Titanic Survival API")

# Add CORS Middleware to ensure frontend can communicate from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input validation model
class Passenger(BaseModel):
    Pclass: int = Field(..., ge=1, le=3, description="Ticket class (1st, 2nd, or 3rd)")
    Sex: str = Field(..., description="Gender of the passenger")
    Age: float = Field(..., ge=0, le=100, description="Age of the passenger")
    SibSp: int = Field(..., ge=0, description="Number of siblings/spouses aboard")
    Parch: int = Field(..., ge=0, description="Number of parents/children aboard")

@app.get("/")
def home():
    return {
        "message": "Titanic EDA API is running",
        "status": "Ready",
        "endpoints": ["/stats/summary", "/analysis/survival-by-class", "/analysis/survival-by-sex", "/analysis/age-dist", "/analysis/survival-by-port", "/predict"]
    }

# Load and clean data globally
try:
    # Use localized path for reliability
    dataset_path = "titanic_data.csv"
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset {dataset_path} not found.")
        
    df = pd.read_csv(dataset_path)
    df['Age'] = df['Age'].fillna(df['Age'].median())
    df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
except Exception as e:
    print(f"Error loading data: {e}")
    df = pd.DataFrame()

# Initialize and train model if data is available
if not df.empty:
    X = pd.get_dummies(df[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch']], columns=['Sex'])
    y = df['Survived']
    model = RandomForestClassifier(n_estimators=100, random_state=42).fit(X, y)
    training_cols = X.columns
else:
    model = None
    training_cols = []

@app.get("/stats/summary")
def get_summary():
    if df.empty:
        raise HTTPException(status_code=503, detail="Dataset not loaded")
    return {
        "survival_rate": round(df['Survived'].mean() * 100, 2),
        "avg_age": round(df['Age'].mean(), 1),
        "total_passengers": int(len(df))
    }

@app.get("/analysis/survival-by-class")
def survival_by_class():
    if df.empty: return []
    return df.groupby('Pclass')['Survived'].mean().reset_index().to_dict(orient="records")

@app.get("/analysis/survival-by-sex")
def survival_by_sex():
    if df.empty: return []
    return df.groupby('Sex')['Survived'].mean().reset_index().to_dict(orient="records")

@app.get("/analysis/age-dist")
def age_dist():
    if df.empty: return {"ages": []}
    return {"ages": df['Age'].tolist()}

@app.get("/analysis/survival-by-port")
def survival_by_port():
    if df.empty: return []
    return df.groupby('Embarked')['Survived'].mean().reset_index().to_dict(orient="records")

@app.post("/predict")
def predict_survival(passenger: Passenger):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not initialized")
    
    # Process Pydantic model to DataFrame
    input_df = pd.DataFrame([passenger.dict()])
    
    # One-hot encoding for Sex
    input_X = pd.get_dummies(input_df, columns=['Sex'])
    
    # Realign with training columns
    for col in training_cols:
        if col not in input_X.columns:
            input_X[col] = 0
    input_X = input_X[training_cols]
    
    prob = model.predict_proba(input_X)[0][1]
    return {"survival_probability": round(float(prob), 4)}