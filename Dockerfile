FROM python:3.8.10-alpine

WORKDIR /app

COPY requirement.txt .

RUN pip install -r requirement.txt

COPY app.py .

EXPOSE 5000

CMD ["/usr/local/bin/flask", "run", "--host=0.0.0.0"]


