FROM python:3.9.7



RUN apt-get update &&


WORKDIR /gamabot

COPY . .

RUN python -m pip install --upgrade pip && \
    pip install -r req.txt

CMD ["python", "client.py"]