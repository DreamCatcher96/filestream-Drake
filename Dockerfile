FROM ubuntu:20.04

WORKDIR /app

RUN apt-get -qq update
ENV TZ Asia/Kolkata
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -qq install -y \
    python3 python3-pip

RUN apt-get install -y software-properties-common
RUN apt-get -y update

RUN apt-get install libpq-dev python3-dev

COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt

COPY . .

CMD ["python3","-m","Adarsh"]