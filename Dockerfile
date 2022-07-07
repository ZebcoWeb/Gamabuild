FROM python:3.9.7


RUN apt update && apt upgrade -y

RUN git clone https://zebcoweb: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@github.com/ZebcoWeb/Gamabuild.git && \
    cd Gamabuild && \
    python -m pip install --upgrade pip && \
    pip install -r req.txt

WORKDIR /Gamabuild

CMD ["python", "run.py"]