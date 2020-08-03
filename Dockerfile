FROM python:3.6-slim
COPY requirements.txt requirements.txt
COPY ./ ./app
WORKDIR ./app
EXPOSE 5000
RUN pip install -r requirements.txt --user
ENTRYPOINT ["python", "run.py"]