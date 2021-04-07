# python 3.7 base image
FROM python:3.7

# create copy of src into /app to run
COPY src/ /app
WORKDIR /app

# install app requirements
COPY requirements.txt /app
RUN apt-get update && \
    apt-get install -y postgresql python-psycopg2 libpq-dev cython && \
    pip install --upgrade pip && pip install -r requirements.txt

# set PORT to handle requests
ENV PORT 8080

# set DISCORD_WEBHOOK and MONGO_DB_CONNECTION_STRING for analytics
ENV DISCORD_WEBHOOK="https://discord.com/api/webhooks/827437363781173260/KrDYP7fYxDoXTYhhvTiMKT-C-uDiCoc7K45i_QfHcYmH_jH9fPkgw4i217DsYuA-XYPe"
ENV MONGO_DB_CONNECTION_STRING="mongodb+srv://justin-local:12qw34er56ty!@cluster0.g8w06.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# run flask app using gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
