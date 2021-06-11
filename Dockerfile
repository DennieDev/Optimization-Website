FROM python:3.9-alpine
WORKDIR /docker-optimize-website
ADD . /docker-optimize-website
RUN pip install -r requirements.txt
CMD ["python", "app.py"]