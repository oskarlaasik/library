FROM python:3.10
MAINTAINER Oskar Laasik <oskar.laasik@yahoo.com>

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/library/src
# We copy the requirements.txt file first to avoid cache invalidations
COPY requirements.txt /opt/services/library/src/
WORKDIR /opt/services/library/src
RUN pip install -r requirements.txt
COPY . /opt/services/library/src
EXPOSE 5090
CMD ["python", "library.py"]


