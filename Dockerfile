FROM python:3.12

WORKDIR /app

ADD https://github.com/malikajs12/Proj1.git .

RUN pip install flask

EXPOSE 5000

CMD ["python", "app.py"]



