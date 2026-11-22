from dataclasses import dataclass
from decimal import Decimal
from datetime import date
@dataclass
class ticket:
    id: int

    transaction_date: int 

    event_id: int 

    event_name: str  

    event_date: date  

    event_type: str

    event_city: str  

    customer_id: int  

    price: Decimal   

    num_tickets: int 

    def __post_init__(self):
        if self.price < 0:
            raise Exception("invalid price") 

    @classmethod
    def from_csv_row(cls, row: list[str]) -> "ticket":
        if len(row) != 10:
            raise ValueError(f"Expected 10 CSV columns, got {len(row)}")

        return cls(
            id=int(row[0]),
            transaction_date=int(date.fromisoformat(row[1].strip()).strftime("%Y%m%d")),
            event_id=int(row[2]),
            event_name=row[3].strip(),
            event_date=date.fromisoformat(row[4].strip()),
            event_type=row[5].strip(),
            event_city=row[6].strip(),
            customer_id=int(row[7]),
            price=Decimal(row[8]),
            num_tickets=int(row[9]),
        )
    