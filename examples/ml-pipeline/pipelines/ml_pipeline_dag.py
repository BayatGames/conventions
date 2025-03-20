"""
ML Pipeline DAG

This Airflow DAG orchestrates the entire machine learning pipeline, from data ingestion
to model deployment and monitoring.
"""

import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.sensors.filesystem import FileSensor
from airflow.models import Variable
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator


# Default arguments
default_args = {
    "owner": "data_science_team",
    "depends_on_past": False,
    "email": ["data-science@example.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "queue": "ml_pipeline",
    "pool": "ml_resources",
}

# Configuration
MODEL_NAME = "{{var.value.model_name}}"
MODEL_VERSION = "{{var.value.model_version}}"
DATA_PATH = "{{var.value.data_path}}"
MLFLOW_TRACKING_URI = "{{var.value.mlflow_tracking_uri}}"
DEPLOYMENT_ENV = "{{var.value.deployment_env}}"

# Define the DAG
dag = DAG(
    "ml_pipeline",
    default_args=default_args,
    description="End-to-end ML pipeline for training and deploying models",
    schedule_interval="0 0 * * *",  # Daily at midnight
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["ml", "production"],
    doc_md=__doc__,
)

# Define tasks
data_validation_sensor = FileSensor(
    task_id="data_validation_sensor",
    filepath=f"{DATA_PATH}/raw_data.csv",
    fs_conn_id="fs_default",
    poke_interval=60,  # Check every minute
    timeout=60 * 60 * 12,  # Timeout after 12 hours
    mode="reschedule",  # Release worker slot between pokes
    dag=dag,
)

def _ingest_data(**context):
    """Task to ingest data from various sources."""
    from ml_pipeline.data.ingest import DataIngestion
    
    # Initialize data ingestion
    ingestion = DataIngestion(
        output_path=f"{DATA_PATH}/ingested",
        log_level="INFO"
    )
    
    # Ingest data from multiple sources
    ingestion.ingest_from_file(f"{DATA_PATH}/raw_data.csv")
    ingestion.ingest_from_database("production_db", "customer_data")
    
    # Save ingested data
    output_file = ingestion.save(f"{DATA_PATH}/processed/data_{context['ts_nodash']}.parquet")
    
    # Log output path for downstream tasks
    context["ti"].xcom_push(key="processed_data_path", value=output_file)
    
    return output_file

ingest_data = PythonOperator(
    task_id="ingest_data",
    python_callable=_ingest_data,
    provide_context=True,
    dag=dag,
)

def _feature_engineering(**context):
    """Task to perform feature engineering."""
    from ml_pipeline.features.transformers import FeatureEngineer
    
    # Get processed data path from upstream task
    processed_data_path = context["ti"].xcom_pull(
        task_ids="ingest_data", key="processed_data_path"
    )
    
    # Initialize feature engineering
    feature_engineer = FeatureEngineer(
        input_path=processed_data_path,
        output_path=f"{DATA_PATH}/features",
        config_path="config/feature_config.yml",
    )
    
    # Generate features
    output_file = feature_engineer.generate_features()
    
    # Log output path for downstream tasks
    context["ti"].xcom_push(key="features_path", value=output_file)
    
    return output_file

feature_engineering = PythonOperator(
    task_id="feature_engineering",
    python_callable=_feature_engineering,
    provide_context=True,
    dag=dag,
)

def _train_model(**context):
    """Task to train the model."""
    from ml_pipeline.training.trainers import ModelTrainer
    
    # Get features path from upstream task
    features_path = context["ti"].xcom_pull(
        task_ids="feature_engineering", key="features_path"
    )
    
    # Initialize model trainer
    trainer = ModelTrainer(
        data_path=features_path,
        model_name=MODEL_NAME,
        model_version=MODEL_VERSION,
        config_path="config/training_config.yml",
        mlflow_tracking_uri=MLFLOW_TRACKING_URI,
    )
    
    # Train model
    run_id, model_uri = trainer.train()
    
    # Log model info for downstream tasks
    context["ti"].xcom_push(key="run_id", value=run_id)
    context["ti"].xcom_push(key="model_uri", value=model_uri)
    
    return run_id

train_model = PythonOperator(
    task_id="train_model",
    python_callable=_train_model,
    provide_context=True,
    dag=dag,
)

def _evaluate_model(**context):
    """Task to evaluate the model."""
    from ml_pipeline.training.evaluation import ModelEvaluator
    
    # Get model info from upstream task
    run_id = context["ti"].xcom_pull(task_ids="train_model", key="run_id")
    
    # Get features path from upstream task
    features_path = context["ti"].xcom_pull(
        task_ids="feature_engineering", key="features_path"
    )
    
    # Initialize model evaluator
    evaluator = ModelEvaluator(
        data_path=features_path,
        run_id=run_id,
        model_name=MODEL_NAME,
        mlflow_tracking_uri=MLFLOW_TRACKING_URI,
    )
    
    # Evaluate model
    metrics = evaluator.evaluate(test_size=0.2)
    
    # Check if accuracy meets threshold for deployment
    should_deploy = metrics.get("accuracy", 0) >= 0.8
    context["ti"].xcom_push(key="should_deploy", value=should_deploy)
    context["ti"].xcom_push(key="metrics", value=metrics)
    
    # Generate evaluation report
    report_path = evaluator.generate_report(
        output_path=f"{DATA_PATH}/reports/evaluation_{context['ts_nodash']}.html"
    )
    context["ti"].xcom_push(key="report_path", value=report_path)
    
    return should_deploy

evaluate_model = PythonOperator(
    task_id="evaluate_model",
    python_callable=_evaluate_model,
    provide_context=True,
    dag=dag,
)

def _deploy_model(**context):
    """Task to deploy the model to production."""
    from ml_pipeline.deployment import ModelDeployer
    
    # Get model info from upstream tasks
    run_id = context["ti"].xcom_pull(task_ids="train_model", key="run_id")
    metrics = context["ti"].xcom_pull(task_ids="evaluate_model", key="metrics")
    
    # Check if we should deploy
    should_deploy = context["ti"].xcom_pull(task_ids="evaluate_model", key="should_deploy")
    if not should_deploy:
        raise ValueError(f"Model metrics do not meet deployment threshold: {metrics}")
    
    # Initialize model deployer
    deployer = ModelDeployer(
        config_path="config/deployment_config.yml",
        mlflow_tracking_uri=MLFLOW_TRACKING_URI,
        deployment_env=DEPLOYMENT_ENV,
    )
    
    # Register model in model registry
    model_info = deployer.register_model(
        run_id=run_id,
        model_name=MODEL_NAME,
        model_version=MODEL_VERSION,
        description=f"Model trained on {context['ts']}",
        metrics=metrics,
    )
    
    # Validate model meets quality standards
    validation_passed = deployer.validate_model(
        model_name=MODEL_NAME,
        validation_data=f"{DATA_PATH}/validation/validation_data.csv",
    )
    
    if not validation_passed:
        raise ValueError("Model validation failed")
    
    # Deploy model
    deployed = deployer.deploy_model(
        model_name=MODEL_NAME,
        set_as_default=True,
        restart_server=True,
    )
    
    context["ti"].xcom_push(key="deployment_success", value=deployed)
    return deployed

deploy_model = PythonOperator(
    task_id="deploy_model",
    python_callable=_deploy_model,
    provide_context=True,
    dag=dag,
)

# Configure monitoring
def _setup_monitoring(**context):
    """Task to setup monitoring for the deployed model."""
    from ml_pipeline.monitoring.collectors.metrics_collector import ModelMetricsCollector
    from ml_pipeline.monitoring.collectors.drift_detector import DriftDetector
    
    # Get model info from upstream tasks
    run_id = context["ti"].xcom_pull(task_ids="train_model", key="run_id")
    
    # Get features path from upstream task
    features_path = context["ti"].xcom_pull(
        task_ids="feature_engineering", key="features_path"
    )
    
    # Setup metrics collector
    metrics_collector = ModelMetricsCollector(
        model_name=MODEL_NAME,
        model_version=MODEL_VERSION,
        metrics_store="prometheus",
        push_gateway_url=os.environ.get("PROMETHEUS_PUSHGATEWAY", "localhost:9091"),
        mlflow_tracking_uri=MLFLOW_TRACKING_URI,
    )
    
    # Setup drift detector with reference data
    drift_detector = DriftDetector(
        model_name=MODEL_NAME,
        model_version=MODEL_VERSION,
        reference_data_path=features_path,
        metrics_store="prometheus",
        push_gateway_url=os.environ.get("PROMETHEUS_PUSHGATEWAY", "localhost:9091"),
    )
    
    return True

setup_monitoring = PythonOperator(
    task_id="setup_monitoring",
    python_callable=_setup_monitoring,
    provide_context=True,
    dag=dag,
)

# Notification task
deployment_notification = SlackWebhookOperator(
    task_id="deployment_notification",
    http_conn_id="slack_webhook",
    webhook_token=Variable.get("slack_webhook_token"),
    message="""
        :rocket: Model Deployment Completed
        *Model:* {{ var.value.model_name }} v{{ var.value.model_version }}
        *Environment:* {{ var.value.deployment_env }}
        *Accuracy:* {{ ti.xcom_pull(task_ids='evaluate_model', key='metrics').get('accuracy', 'N/A') }}
        *F1 Score:* {{ ti.xcom_pull(task_ids='evaluate_model', key='metrics').get('f1_score', 'N/A') }}
        *Deployed:* {{ ti.xcom_pull(task_ids='deploy_model', key='deployment_success') }}
        *Date:* {{ ds }}
    """,
    trigger_rule=TriggerRule.ALL_DONE,  # Send notification regardless of upstream task status
    dag=dag,
)

# Define task dependencies
data_validation_sensor >> ingest_data
ingest_data >> feature_engineering
feature_engineering >> train_model
train_model >> evaluate_model
evaluate_model >> deploy_model
deploy_model >> setup_monitoring
deploy_model >> deployment_notification
setup_monitoring >> deployment_notification

if __name__ == "__main__":
    dag.cli() 