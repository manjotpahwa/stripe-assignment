import inventory
import logging


class Cart:
    def __init__(self, items=None):
        logging.debug('Creating cart')
        self.cart_items = items or {}

    def get_total(self):
        total = 0
        for item_id, item_val in self.cart_items.items():
            total += item_val['price'] * item_val['qty']

        return total

    def get_items(self):
        return self.cart_items

    def set_items(self, items):
        self.cart_items = items

