FROM bitnami/python:3.9

COPY . /github_activity_analysis_service

ENV APP_ROOT=/github_activity_analysis_service

WORKDIR /github_activity_analysis_service

RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install --upgrade pip && apt-get update -y
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]

