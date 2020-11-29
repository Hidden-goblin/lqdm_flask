FROM python:3.8-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 
RUN pip install -r requirements.txt 
EXPOSE 5000
COPY . .
RUN python setup.py install
CMD ["waitress-serve", "--port=5000", "--call", "app:create" ]