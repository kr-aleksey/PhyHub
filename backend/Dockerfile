FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
COPY . /app
CMD ["gunicorn", "PhyHub.wsgi:application", "--bind", "0:8000"]
