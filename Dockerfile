FROM python:3.10

RUN mkdir .docker
RUN python3 -m pip freeze > .docker/requirements.txt
RUN python3 -m pip install -r .docker/requirements.txt

CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]




 



  

  