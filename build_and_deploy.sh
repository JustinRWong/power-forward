cd server

gcloud builds submit --tag gcr.io/power-forward/flask-fire

gcloud beta run deploy  core-flask-server --image gcr.io/power-forward/flask-fire --platform=managed --region=us-west1 --ingress=all
