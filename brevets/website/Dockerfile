FROM python:3.8
LABEL maintainer="olegv@uoregon.edu"
COPY . /website
WORKDIR /website
RUN pip install -r requirements.txt
CMD ["python", "website.py"]
