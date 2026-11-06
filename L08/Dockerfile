FROM python:3.14.7

WORKDIR /app

COPY inventory-management.py .
COPY inventory.json .
COPY product.py .
COPY inventory.py .
COPY canbeshipped.py .
COPY physicalproduct.py .
COPY digitalproduct.py .
COPY supplier.py .
COPY order.py .
COPY orderline.py .

CMD ["python", "inventory-management.py"]
