# Local Setup Guide for Advisor Copilot

## Prerequisites

1. **Python Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **GCP Setup**
   ```bash
   # Install Google Cloud SDK if not already installed
   curl https://sdk.cloud.google.com | bash
   
   # Login to GCP
   gcloud auth login
   gcloud config set project even-ruler-467916-q3
   gcloud auth application-default login
   
   # Set your project
   gcloud config set project even-ruler-467916-q3
   ```
   # Credentials are stored here
   /home/prakashb/.config/gcloud/application_default_credentials.json

3. **Enable Required APIs**
   ```bash
   # Enable required GCP APIs
   gcloud services enable bigquery.googleapis.com
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable run.googleapis.com
   ```

4. **BigQuery Setup**
   ```sql
   -- Create dataset
   CREATE DATASET IF NOT EXISTS financial_advisor;
   
   -- Create table
   CREATE TABLE financial_advisor.customer_portfolio (
     customer_id STRING,
     asset_class STRING,
     sub_category STRING,
     amount FLOAT64,
     last_updated TIMESTAMP
   );
   
   -- Sample data
   INSERT INTO financial_advisor.customer_portfolio
   VALUES ('test123', 'Equity', 'Large-cap', 800000, CURRENT_TIMESTAMP());
   ```

5. **Environment Variables**
   - Verify `.env` file has correct values:
     - PROJECT_ID=even-ruler-467916-q3
     - LOCATION=us-central1
     - MODEL_NAME=gemini-1.5-pro-preview
     - BQ_DATASET=financial_advisor

## Running Locally

1. **Start the Server**
   ```bash
   source venv/bin/activate
   pip install -e .
   python api/main.py
   ```

2. **Test the API**
   ```bash
   curl -X POST http://localhost:8080/advice \
     -H "Content-Type: application/json" \
     -d '{
       "customer_id": "test123",
       "query": "What is my risk exposure?"
     }'
   ```

## Troubleshooting

1. **Authentication Issues**
   ```bash
   # Reset credentials if needed
   gcloud auth application-default revoke
   gcloud auth application-default login
   ```

2. **Module Not Found**
   ```bash
   # Install package in dev mode
   pip install -e .
   ```

## Troubleshooting

1. **Authentication Issues**
   ```bash
   # Reset credentials if needed
   gcloud auth application-default revoke
   gcloud auth application-default login
   ```

2. **Module Not Found**
   ```bash
   # Install package in dev mode
   pip install -e .
   ```

3. **Vertex AI Generative AI Issues**
   ```bash
   # Update google-cloud-aiplatform to latest version that supports Gemini
   pip uninstall google-cloud-aiplatform
   pip install google-cloud-aiplatform>=1.40.0
   
   # If still getting generative_models error, try:
   pip install --upgrade google-ai-generative-language
   ```