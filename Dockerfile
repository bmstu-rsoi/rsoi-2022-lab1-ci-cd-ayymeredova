FROM python:3.9.6

ENV PORT=8080


COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
RUN chmod 644 app.py
CMD ["app.py"]


