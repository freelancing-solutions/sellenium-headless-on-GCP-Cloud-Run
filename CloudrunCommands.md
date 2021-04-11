# build command
gcloud builds submit --tag "gcr.io/pinoydesk/sellenium"

# list images
gcloud container images list

# deploy images
gcloud run deploy sellenium --image "gcr.io/pinoydesk/sellenium" --platform managed --allow-unauthenticated

# setting region
gcloud config set run/region asia-east2

# setting IAM Policy
gcloud beta run services add-iam-policy-binding --region=asia-east2 --member=allUsers --role=roles/run.invoker sellenium