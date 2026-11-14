from dataclasses import dataclass
from decimal import Decimal
@dataclass
class ticket:
    id: int

    transaction_date: int 

    event_id: int 

    event_name: str  

    event_date: str  

    event_city: str  

    customer_id: int  

    price: Decimal   

    num_tickets: int 

    def __post_init__(self):
        if self.price < 0:
            raise Exception("invalid price") 
