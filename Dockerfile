FROM python:3.9-alpine
WORKDIR /docker-optimize-website
ADD . /docker-optimize-website
RUN apk --no-cache add gcc musl-dev
RUN pip install -r requirements.txt
CMD ["python", "app.py"]