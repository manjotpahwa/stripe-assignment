import inventory


class Cart:
    def __init__(self, items=None):
        print('Creating cart')
        self.items = items or {}
        print(self.items)

    def get_total(self):
        total = 0
        for item_id, item_val in self.items.items():
            total += item_val['price'] * item_val['qty']

        return total

    def get_items(self):
        return self.items
