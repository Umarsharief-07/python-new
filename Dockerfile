FROM python:3

WORKDIR /app

COPY requirements.txt .

# Fail on purpose
RUN pip install --no-cache-dir -r requirements.txt && exit 1

COPY python.py .

EXPOSE 5000

CMD ["python", "python.py"]
