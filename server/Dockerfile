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

# set DISCORD_WEBHOOK for analytics
ENV DISCORD_WEBHOOK https://discord.com/api/webhooks/827437363781173260/KrDYP7fYxDoXTYhhvTiMKT-C-uDiCoc7K45i_QfHcYmH_jH9fPkgw4i217DsYuA-XYPe

# run flask app using gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
