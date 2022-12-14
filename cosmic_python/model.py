from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class OrderLine:
    orderid: int
    sku: str
    quantity: int

class Batch:
    def __init__(self, ref: str, sku: str, quantity: int, eta: Optional[date]) -> None:
        self.reference = ref
        self.sku = sku
        self._purchased_quantity = quantity
        self._allocations = set() # type: Set[OrderLine]
    
    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)
    
    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.quantity
