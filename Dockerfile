FROM python:3.10

RUN mkdir app
COPY app/requirements.txt .

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install gunicorn

EXPOSE 8050/tcp

CMD ["python3", "app.py"]