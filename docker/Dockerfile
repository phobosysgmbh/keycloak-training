FROM python:3.10-slim
WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends -y git && \
    pip3.10 install gunicorn[gevent] && \
    pip3.10 install gevent && \
    rm -rf /var/cache/apt


COPY app /app
COPY requirements.txt /app/requirements.txt

RUN pip3.10 install -r requirements.txt

COPY public /public

EXPOSE 5000

CMD /app/run-server.sh
