# Production Deployment Guide for Advisor Copilot

## Prerequisites

1. **Enable Required APIs** (if not already enabled)
   ```bash
   gcloud services enable \
     cloudbuild.googleapis.com \
     run.googleapis.com \
     containerregistry.googleapis.com \
     artifactregistry.googleapis.com
   ```

2. **Service Account Setup**
   ```bash
   # Create service account
   gcloud iam service-accounts create advisor-copilot-sa \
     --display-name="Advisor Copilot Service Account"
   
   # Add required roles
   gcloud projects add-iam-policy-binding even-ruler-467916-q3 \
     --member="serviceAccount:advisor-copilot-sa@even-ruler-467916-q3.iam.gserviceaccount.com" \
     --role="roles/bigquery.dataViewer"
   
   gcloud projects add-iam-policy-binding even-ruler-467916-q3 \
     --member="serviceAccount:advisor-copilot-sa@even-ruler-467916-q3.iam.gserviceaccount.com" \
     --role="roles/aiplatform.user"
   
   gcloud projects add-iam-policy-binding even-ruler-467916-q3 \
     --member="serviceAccount:advisor-copilot-sa@even-ruler-467916-q3.iam.gserviceaccount.com" \
     --role="roles/bigquery.jobUser"
   ```

3. **Docker & Artifact Registry Setup**
   ```bash
   # Create Artifact Registry repository
   gcloud artifacts repositories create advisor-copilot \
     --repository-format=docker \
     --location=us-central1 \
     --description="Advisor Copilot Docker repository"

   # Configure Docker auth
   gcloud auth configure-docker us-central1-docker.pkg.dev

   # Build container
   docker build -t us-central1-docker.pkg.dev/even-ruler-467916-q3/advisor-copilot/api:v1 .
   
   # Push to Artifact Registry
   docker push us-central1-docker.pkg.dev/even-ruler-467916-q3/advisor-copilot/api:v1
   ```

## Deployment Steps

1. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy advisor-copilot \
     --image us-central1-docker.pkg.dev/even-ruler-467916-q3/advisor-copilot/api:v1 \
     --platform managed \
     --region us-central1 \
     --memory 1Gi \
     --cpu 1 \
     --min-instances 0 \
     --max-instances 10 \
     --service-account advisor-copilot-sa@even-ruler-467916-q3.iam.gserviceaccount.com \
     --set-env-vars PROJECT_ID=even-ruler-467916-q3,LOCATION=us-central1,MODEL_NAME=gemini-2.0-flash-lite-001,BQ_DATASET=financial_advisor
   ```

2. **Set IAM Permissions**
   ```bash
   # Allow authenticated users only (recommended for production)
   gcloud run services add-iam-policy-binding advisor-copilot \
     --member="serviceAccount:advisor-copilot-sa@even-ruler-467916-q3.iam.gserviceaccount.com" \
     --role="roles/run.invoker" \
     --region=us-central1
   
   # Or allow public access (not recommended for production)
   # gcloud run services add-iam-policy-binding advisor-copilot \
   #   --member="allUsers" \
   #   --role="roles/run.invoker" \
   #   --region=us-central1
   ```

3. **Test Production Endpoint**
   ```bash
   # Get the service URL
   SERVICE_URL=$(gcloud run services describe advisor-copilot --format='value(status.url)')
   
   # For authenticated access, get ID token
   TOKEN=$(gcloud auth print-identity-token)
   
   # Test the endpoint
   curl -X POST $SERVICE_URL/advice \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "customer_id": "test123",
       "query": "what is my net worth"
     }'
   ```

## Monitoring & Maintenance

1. **View Logs**
   ```bash
   # View real-time logs (streaming)
   gcloud beta logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=advisor-copilot"
   
   # Or view recent logs
   gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=advisor-copilot" --limit=50
   
   # Search specific errors
   gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=advisor-copilot AND severity>=ERROR" --limit=10
   ```

2. **Monitor Performance**
   - Cloud Run Dashboard
     - Navigate to [Cloud Run Console](https://console.cloud.google.com/run)
     - Monitor:
       - Request latency
       - Memory usage
       - CPU utilization
       - Concurrent requests
       - Error rates

3. **Set Up Alerts**
   ```bash
   # Create error rate alert
   gcloud alpha monitoring channels create \
     --display-name="Advisor-Copilot-Alerts" \
     --type=email \
     --email-address=your-email@domain.com
   ```

## Cost Management

1. **Budget Alerts**
   ```bash
   # Set up budget alert
   gcloud billing budgets create \
     --billing-account=YOUR_BILLING_ACCOUNT_ID \
     --display-name="Advisor Copilot Budget" \
     --budget-amount=1000 \
     --threshold-rule=percent=0.5 \
     --threshold-rule=percent=0.75 \
     --threshold-rule=percent=0.9
   ```

2. **Cost Optimization**
   - Monitor and adjust:
     - Cloud Run instance count (min/max)
     - Memory allocation
     - CPU allocation
     - Vertex AI model usage
     - BigQuery query optimization

3. **Cleanup Unused Resources**
   ```bash
   # Stop Cloud Run service when not in use
   gcloud run services delete advisor-copilot --region=us-central1

   # Delete Artifact Registry repository if not needed
   gcloud artifacts repositories delete advisor-copilot \
     --location=us-central1

   # Delete unused service account
   gcloud iam service-accounts delete \
     advisor-copilot-sa@even-ruler-467916-q3.iam.gserviceaccount.com

   # Optional: Delete BigQuery dataset if it's just for testing
   bq rm -r -f financial_advisor
   ```

   Key resources that incur costs:
   - Cloud Run service (minimal when idle, but still charges for any requests)
   - Vertex AI API calls (charged per request)
   - BigQuery storage and queries
   - Artifact Registry storage

   To minimize costs during development:
   1. Delete Cloud Run service when not actively testing
   2. Keep min-instances at 0
   3. Clean up test data in BigQuery
   4. Remove unused container images from Artifact Registry

## Rollback Procedure

1. **Quick Rollback to Previous Version**
   ```bash
   # List revisions
   gcloud run revisions list --service=advisor-copilot --region=us-central1
   
   # Rollback to specific revision
   gcloud run services update-traffic advisor-copilot \
     --to-revision=advisor-copilot-00001-abc \
     --region=us-central1
   ```
