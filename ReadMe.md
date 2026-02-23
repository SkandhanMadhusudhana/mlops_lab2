# Lab 2: Dockerized Iris Classifier API

This lab demonstrates how to containerize a Machine Learning model (Gradient Boosting Classifier) and serve it using FastAPI.

## Overview
The application trains a model on the Iris dataset at startup and serves predictions via a REST API.

## detailed Instructions

### 1. Build the Docker Image
Build the image using the `Dockerfile` in the current directory. We use the tag `lab1:v2`.
```bash
docker build -t lab1:v2 .
```

### 2. Run the Container
Run the container, mapping port 8000 of the container to port 8000 on your host.
```bash
docker run -p 8000:8000 lab1:v2
```

### 3. Test the API
You can test the `/predict` endpoint using `curl` or any API client (like Postman).

**Request:**
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

**Expected Response:**
```json
{"prediction": 0, "class_name": "setosa"}
```

---

## Changes Made

### 1. Code Refactoring (`src/main.py`)
- **Model Upgrade**: Replaced `RandomForestClassifier` with `GradientBoostingClassifier`.
- **API Implementation**: Added `FastAPI` to serve predictions via a POST endpoint.
- **Logging**: Replaced `print` statements with standard `logging`.
- **Startup**: Model training happens on application startup.

### 2. Docker Optimization (`Dockerfile`)
- **Base Image**: Switched to `python:3.10-slim` for a smaller footprint.
- **Caching**: Reordered `COPY` steps to install dependencies before copying source code, speeding up builds.
- **Security**: Added a non-root `appuser`.
- **Network**: Exposed port 8000 and configured `uvicorn` entrypoint.

### 3. Dependencies (`src/requirements.txt`)
- Added `fastapi` and `uvicorn`.
