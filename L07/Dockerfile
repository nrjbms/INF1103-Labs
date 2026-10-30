FROM python:3.14.7

WORKDIR /app

COPY inventory-management.py .
COPY inventory.json .
COPY product.py .
COPY inventory.py .
COPY canbeshipped.py .
COPY physicalproduct.py .
COPY digitalproduct.py .

CMD ["python", "inventory-management.py"]
