import typeguard


class Quantity:
    @typeguard.typechecked
    def __init__(self, amount: int, max_amount: int) -> None:
        self.amount: int = amount
        self.max_amount: int = max_amount

    @typeguard.typechecked
    def is_empty(self) -> bool:
        return self.amount == 0

    @typeguard.typechecked
    def is_full(self) -> bool:
        return self.amount == self.max_amount

    @typeguard.typechecked
    def expend(self, amount: int) -> bool:
        if amount > self.amount:
            return False
        self.amount -= amount
        return True

    @typeguard.typechecked
    def replenish(self, amount: int) -> bool:
        if amount > (self.max_amount - self.amount):
            return False
        self.amount += amount
        return True

    @typeguard.typechecked
    def refill(self) -> int:
        amount_filled: int = self.max_amount - self.amount
        self.amount += amount_filled
        return amount_filled
