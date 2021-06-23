FROM python:3

COPY . /opt/source-code
WORKDIR /opt/source-code
RUN pip3 --no-cache-dir install -r requirements.txt
RUN apt-get update
RUN apt-get install -y locales locales-all
ENV LC_TIME de_DE.UTF-8

ENTRYPOINT ["python3"]
CMD ["bot.py"]