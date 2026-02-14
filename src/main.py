import logging
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import joblib
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Global variable to hold the model
model = None
MODEL_PATH = 'iris_model.pkl'

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.on_event("startup")
def load_or_train_model():
    global model
    
    # Load the Iris dataset
    logger.info("Loading Iris dataset...")
    iris = load_iris()
    X, y = iris.data, iris.target

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Gradient Boosting Classifier
    logger.info("Training GradientBoostingClassifier...")
    model = GradientBoostingClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    accuracy = model.score(X_test, y_test)
    logger.info(f"Model trained. Accuracy: {accuracy:.4f}")

    # Save the model
    joblib.dump(model, MODEL_PATH)
    logger.info(f"Model saved to {MODEL_PATH}")

@app.post("/predict")
def predict(input_data: IrisInput):
    if model is None:
        return {"error": "Model not ready"}
    
    features = [[
        input_data.sepal_length,
        input_data.sepal_width,
        input_data.petal_length,
        input_data.petal_width
    ]]
    
    prediction = model.predict(features)
    return {"prediction": int(prediction[0]), "class_name": ["setosa", "versicolor", "virginica"][prediction[0]]}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
