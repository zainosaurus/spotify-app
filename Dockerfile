FROM python:latest

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD flask run