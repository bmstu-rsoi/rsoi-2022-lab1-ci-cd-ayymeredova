FROM python:3.9.6

ENV PORT=8080


COPY . /app
WORKDIR /app
ENV set FLASK_APP=main.py
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]

CMD ["flask", "run"]


