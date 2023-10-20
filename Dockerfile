FROM python:3
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT FLASK_APP=app.py flask run -h 0.0.0.0