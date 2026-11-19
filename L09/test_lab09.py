from discountstrategy import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount
from productfactory import ProductFactory
from supplier import Supplier
from order import Order
from orderline import OrderLine
from inventory import Inventory

print('Discount Strategies Test')
print('No discount:', NoDiscount().apply(250))           # Expected: 250
print('10% discount:', PercentageDiscount(10).apply(250)) # Expected: 225
print('Bulk discount:', BulkDiscount(200, 20).apply(250)) # Expected: 230
print('Student discount:', StudentDiscount().apply(250)) # Expected: 237.5

print('\nProduct Factory Test')
supplier = Supplier('S1', 'Test Supplier', 'test@example.com')
physical = ProductFactory.create('physical', 'P1', 'Desk Lamp', 25, 10, supplier, weight=2)
digital = ProductFactory.create('digital', 'D1', 'Photo Editor', 49.90, 100, supplier, download_size=500)
print(physical.get_fulfilment_info())  # Expected: Requires physical shipping.
print(digital.get_fulfilment_info())   # Expected: Delivered digitally.

print('\nOrder Discounts Test')
order = Order('O1', BulkDiscount(20, 5))
order.add_order_line(physical, 2)
print('Bulk discounted total:', order.calculate_total()) # Expected: 45
order.set_discount(PercentageDiscount(10))
print('Percentage discounted total:', order.calculate_total()) # Expected: 45
order.set_discount(NoDiscount())
print('Original total:', order.calculate_total()) # Expected: 50

print('\nProduct Type Test')
try:
    ProductFactory.create('service', 'S2', 'Installation', 30, 5, supplier)
except ValueError as error:
    print('Error caught:', error)

print('\nnvalid Price')
try:
    ProductFactory.create('physical', 'P2', 'Bad Product', -10, 5, supplier)
except ValueError as error:
    print('Error caught:', error)

print('\nInvalid Stock')
try:
    ProductFactory.create('digital', 'D2', 'Bad Stock', 10, -5, supplier)
except ValueError as error:
    print('Error caught:', error)

print('\nInvalid Order Quantity')
try:
    OrderLine(physical, 0)
except ValueError as error:
    print('Error caught:', error)

print('\nInventory Test')
inventory = Inventory()
inventory.add_product(physical)
inventory.add_product(digital)
print('Number of products:', len(inventory.get_products())) # Expected: 2


