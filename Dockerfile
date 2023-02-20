FROM python:3.9.7


RUN apt update && apt upgrade -y

WORKDIR /Gamabuild
COPY . .

RUN  python -m pip install --upgrade pip && \
    pip install -r req.txt

CMD ["python", "run.py"]