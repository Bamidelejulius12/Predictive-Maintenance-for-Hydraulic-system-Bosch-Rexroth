# Predictive Maintenance for Hydraulic Systems (Bosch Rexroth Inspired)

## Overview

This project implements an end-to-end predictive maintenance system for hydraulic systems, inspired by industrial applications such as those from Bosch Rexroth AG. The system leverages machine learning techniques to predict equipment degradation and estimate Remaining Useful Life (RUL) using sensor data.

The goal is to transition from reactive maintenance to predictive maintenance by providing real-time insights into machine health, reducing downtime, and improving operational efficiency.

---

## Problem Statement

In manufacturing environments, unexpected machine failures lead to:

* Unplanned downtime
* Increased maintenance costs
* Reduced production efficiency

Traditional maintenance strategies are either reactive or scheduled, both of which are inefficient. Predicting the Remaining Useful Life (RUL) of machines allows organizations to make informed maintenance decisions before failures occur.

---

## Solution

This project provides a production-ready pipeline that:

* Processes raw hydraulic sensor data
* Performs feature engineering and validation
* Trains multiple machine learning models for RUL prediction
* Tracks experiments and models using MLflow
* Stores datasets and features in AWS S3
* Deploys the trained model as a FastAPI service
* Automates deployment using Docker, AWS ECR, and EC2
* Implements CI/CD for continuous integration and delivery

---

## System Architecture

The system consists of the following components:

1. Data Pipeline

   * Data validation
   * Data preprocessing
   * Feature engineering

2. Model Training Pipeline

   * Model training (Random Forest, Gradient Boosting, Linear Regression)
   * Model evaluation
   * Experiment tracking with MLflow

3. Model Registry

   * MLflow + DagsHub for versioning and tracking

4. Storage Layer

   * AWS S3 for datasets, features, and artifacts

5. API Layer

   * FastAPI application for real-time inference

6. Deployment Pipeline

   * Docker for containerization
   * AWS ECR for image storage
   * AWS EC2 for hosting
   * GitHub Actions for CI/CD automation

---

## Tech Stack

* Python
* Scikit-learn
* FastAPI
* MLflow
* DagsHub
* AWS S3
* AWS ECR
* AWS EC2 (Ubuntu)
* Docker
* GitHub Actions
* IAM Roles

---

## Key Features

* End-to-end MLOps pipeline
* Real-time RUL prediction API
* Experiment tracking and model versioning
* Cloud-native deployment on AWS
* Secure authentication using IAM roles
* Automated CI/CD pipeline

---

## API Endpoints

### Health Check

```
GET /
```

Returns API status.

### System Health

```
GET /health
```

Checks if model and dataset are loaded.

### Train Model

```
POST /train
```

Triggers model retraining and reloads artifacts.

### Predict RUL

```
POST /predict
```

Request body:

```
{
  "machine_id": "string",
  "pressure_bar": float,
  "temp_celsius": float,
  "flow_lpm": float,
  "vibration_x_g": float,
  "vibration_y_g": float,
  "pump_rpm": float
}
```

---

## Deployment

The application is deployed using a CI/CD pipeline:

1. Code is pushed to the main branch
2. GitHub Actions builds the Docker image
3. Image is pushed to AWS ECR
4. EC2 pulls the latest image
5. Container is restarted with updated version

---

## Security

* IAM roles are used for EC2 to access AWS services securely
* No hardcoded AWS credentials in the application

---

## Use Case Impact

* Enables predictive maintenance
* Reduces unexpected machine failures
* Improves operational efficiency
* Supports data-driven maintenance strategies

---

## Future Improvements

* Asynchronous model loading and caching
* Monitoring and logging with CloudWatch
* Model performance monitoring in production
* Auto-scaling deployment using Kubernetes or ECS
* Streaming data ingestion for real-time pipelines

---

## Author

Developed and guided by Julius Babatunde as part of a practical MLOps and industrial AI system implementation.

