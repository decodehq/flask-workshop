FROM python:3.9.5
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD flask run --host 0.0.0.0