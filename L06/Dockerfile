FROM python:3.14.7

WORKDIR /app

COPY inventory_management.py .
COPY inventory.json .
COPY product.py .
COPY inventory.py .

CMD ["python", "inventory_management.py"]
