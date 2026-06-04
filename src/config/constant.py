import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
equipment_data = os.path.join(BASE_DIR, "Dataset", "equipment_master.csv")
failure_data = os.path.join(BASE_DIR, "Dataset", "failure_labels.csv")
sensor_data = os.path.join(BASE_DIR, "Dataset", "sensor_telemetry.csv")
maintenance_data = os.path.join(BASE_DIR, "Dataset", "maintenance_log.csv")

cleaned_data = os.path.join(BASE_DIR, "Dataset", "cleaned_data", "bosch_rexroth_cleaned.csv")
featured_data_path = os.path.join(BASE_DIR, "Dataset", "final_data", "rul_featured.csv")
featured_data_json = os.path.join(BASE_DIR, "Dataset", "final_data", "feature_sets.json")


BUCKET_NAME = "brosch-predictive-maintenance"
S3_ARTIFACT_ROOT = f"s3://{BUCKET_NAME}/mlflow-artifacts"
DAGSHUB_OWNER = "babatundejulius911"
DAGSHUB_REPO  = "Predictive-Maintenance-for-Hydraulic-system-Bosch-Rexroth"
EXPERIMENT = "hydraulic-rul-prediction"

