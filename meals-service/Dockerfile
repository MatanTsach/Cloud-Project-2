FROM python:3.8-alpine
WORKDIR /app
COPY . /app
EXPOSE 8000

RUN pip install -r requirements.txt

ENV FLASK_APP=Main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000
CMD ["python3", "App.py"]
