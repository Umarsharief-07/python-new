FROM python:3

WORKDIR /app

COPY requirements.txt .

# FAIL at build time on purpose
RUN pip install --no-cache-dir -r requirements.txt && exit 1

COPY python.py .

EXPOSE 5000

# FAIL at runtime on purpose
CMD ["sh", "-c", "echo 'Failing container at runtime on purpose' && exit 1"]
