FROM python:3.12-slim
RUN groupadd -r groupbookcamp && useradd -r -g groupbookcamp siteuser

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

WORKDIR /app/site/api_app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

USER siteuser