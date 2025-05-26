import threading

class SharedMoney:
    def __init__(self, amount=0):
        self.value = amount
        self.lock = threading.Lock()

    def get(self):
        with self.lock:
            return self.value

    def set(self, amount):
        with self.lock:
            self.value = amount

    def add(self, amount):
        with self.lock:
            self.value += amount

    def subt(self, amount):
        with self.lock:
            if amount > self.value:
                raise ValueError("Cannot subtract more than the current value.")
            self.value -= amount
    def to_dict(self):
        return {"value": self.value}

    @staticmethod
    def from_dict(data):
        return SharedMoney(amount=data.get("value", 0))