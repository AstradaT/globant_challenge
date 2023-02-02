FROM alpine:latest
RUN apk update
RUN apk add py-pip
RUN apk add make automake gcc g++ subversion python3-dev
RUN pip install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install -r requirements.txt
CMD ["python3", "main.py"]