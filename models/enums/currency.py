from enum import Enum

class Currency(str, Enum):
    usd = "USD"
    egp = "EGP"
    aed = "AED"
    yen = "YEN"