import logging
import os
from functools import reduce

class Inventory:
    def __init__(self):
        self.skus = [
                '2LTTufVZkd', 'fXR0woE2TL', '00VxgN9rqx', 'B94gWJOXxy',
                'ooVPl4gvmR', 'fgP9eqP27w', 'aYXQ5WOQJS', 'tcscXY8GA8',
                'A1OSB4bhiI', '4Fkbz2lhYz'
        ]
        self.products = {
                '2LTTufVZkd': {'name': 'Nike Fly Zoom', 'brand': 'Nike', 'qty': 3, 'price': 150},
                'fXR0woE2TL': {'name': 'Asics Nimbus 16', 'brand': 'Asics',
                    'qty':5, 'price': 160},
                '00VxgN9rqx': {'name': 'Nike Fly Knit', 'brand': 'Nike', 'qty': 3, 'price': 150},
                'B94gWJOXxy': {'name': 'Nike Air Max', 'brand': 'Nike', 'qty':
                    0, 'price': 150},
                'ooVPl4gvmR': {'name': 'Nike Ultra Boost', 'brand': 'Nike',
                    'qty': 3, 'price': 250},
                'fgP9eqP27w': {'name': 'Asics Kayano', 'brand': 'Asics', 'qty': 3, 'price': 150},
                'aYXQ5WOQJS': {'name': 'Skechers Razor', 'brand': 'Skechers',
                    'qty': 3, 'price': 250},
                'tcscXY8GA8': {'name': 'Asics Metaride', 'brand': 'Asics', 'qty': 3, 'price': 150},
                'A1OSB4bhiI': {'name': 'Nike Joyride', 'brand': 'Nike', 'qty':
                    10, 'price': 150},
                '4Fkbz2lhYz': {'name': 'Allbirds Knit', 'brand': 'Allbirds',
                    'qty': 3, 'price':100}
                }

    def get_products_in_stock(self):
        stock = {}
        for (k, v) in self.products.items():
            if v['qty'] > 0:
                stock[k] = v
        return stock

    def product_exists(self, item):
        logging.debug('Checking if product exists')
        sku = item['id']
        qty = item['qty']
        if sku in self.skus and item['qty'] <= self.products[sku]['qty']:
            return True
        return False

    def get_cost(self, item):
        logging.debug('Getting single product cost')
        return item['qty'] * self.products[item['id']]['price']

    def get_item(self, item_id):
        logging.debug('Returning item with id ' + item_id)
        return self.products[item_id]

    def get_products_total_cost(self, items):
        logging.debug('Calculating total cost')
        total = 0
        for item in items:
            if self.product_exists(item):
                total += self.get_cost(item)
        return total

    def update_inventory(self, cart):
        items_dict = cart.get_items()
        for item_id, item_val in items_dict.items():
            self.products[item_id]['qty'] -= item_val['qty']
