import inventory



class Cart:
    def __init__(self):
        self.items = []

    def get_total(self):
        total = 0
        for item in self.items():

