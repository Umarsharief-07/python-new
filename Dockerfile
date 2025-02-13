FROM python:3

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY python.py .

EXPOSE 5656

CMD ["python", "python.py"]