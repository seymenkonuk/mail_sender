# Python 3.9 tabanlı bir imaj kullan
FROM python:3.9-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Çalıştırma
ENTRYPOINT ["python"]
CMD ["src/main.py"]
