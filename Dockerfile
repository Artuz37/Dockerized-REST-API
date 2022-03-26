FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
# Install py39 from deadsnakes repository
    apt-get install python3.9 -y && \
# Install pip from standard ubuntu packages
    apt-get install python3-pip -y

COPY app /app
WORKDIR /app

EXPOSE 8000:8000

RUN pip install -r requirements.txt

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]