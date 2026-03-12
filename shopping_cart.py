class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, name: str, price: float, quantity: int = 1):
        if price < 0:
            raise ValueError("Price cannot be negative")
        if name in self.items:
            self.items[name]["quantity"] += quantity
        else:
            self.items[name] = {"price": price, "quantity": quantity}

    def remove_item(self, name: str):
        if name not in self.items:
            raise KeyError(f"{name} not in cart")
        del self.items[name]

    def get_total(self) -> float:
        return sum(v["price"] * v["quantity"] for v in self.items.values())

    def apply_discount(self, percent: float) -> float:
        if not 0 <= percent <= 100:
            raise ValueError("Discount must be between 0 and 100")
        return self.get_total() * (1 - percent / 100)

    def item_count(self) -> int:
        return sum(v["quantity"] for v in self.items.values())