FROM python:slim-buster
ENV FLASK_APP=blog
WORKDIR /app
COPY . .
RUN python setup.py develop
EXPOSE 5000
ENTRYPOINT ["flask", "run", "-h", "0.0.0.0"]
