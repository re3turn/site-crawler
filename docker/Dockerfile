FROM python:3.10 as builder

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt


FROM python:3.10-slim as service
WORKDIR /service
ENV PYTHON_VERSION 3.10
COPY --from=builder /usr/local/lib/python${PYTHON_VERSION}/site-packages /usr/local/lib/python${PYTHON_VERSION}/site-packages

COPY app /service/app
COPY run.py /service

ENTRYPOINT ["python", "/service/run.py"]

