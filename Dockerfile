FROM  python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
        && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/instance

EXPOSE 5006

CMD ["python", "app.py"]
# CMD python app.py working as well
