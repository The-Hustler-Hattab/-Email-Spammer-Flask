# Deploy the app to GCP Cloud Run
docker build -t email-spammer:latest .

# Tag the Docker image
docker tag email-spammer:latest gcr.io/personal-projects-416300/email-spammer:latest

# Push the Docker image to Google Container Registry (GCR)
docker push gcr.io/personal-projects-416300/email-spammer:latest

# Deploy the app to Cloud Run
gcloud run deploy email-spammer `
  --image gcr.io/personal-projects-416300/email-spammer:latest `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --cpu 1 `
  --memory 1Gi `
  --port=5000 `
  --project=personal-projects-416300