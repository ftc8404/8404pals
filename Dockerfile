FROM tiangolo/uwsgi-nginx-flask:python3.7

LABEL Name=quixilver8404data Version=0.0.1
ENV LISTEN_PORT 5000
EXPOSE 5000

#Copy ODBC config
COPY odbcinst.ini /etc/odbcinst.ini

#Install FreeTDS and dependencies for PyODBC
RUN apt-get update && apt-get install -y tdsodbc unixodbc-dev \
    && apt install unixodbc-bin -y  \
    && apt-get clean -y

COPY ./app /app

RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r /app/requirements.txt