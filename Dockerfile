FROM python:3.9.6

COPY src/ /app/
WORKDIR /app

RUN pip install -r requirements.txt
# ENV set FLASK_APP=main.py

CMD ["python", "main.py"]