FROM python:3

COPY . /opt/source-code
WORKDIR /opt/source-code
RUN pip3 --no-cache-dir install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["bot.py"]