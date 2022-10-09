from lib.config import *
from lib.helpers import get_front_month, next_two_months
from lib.price_management import Price

front_month = get_front_month()
FMp1, FMp2 = next_two_months(front_month)

def create_prices():

    prices = [
        Price(ticker=BZ,
                month=front_month,
                desc="BZ FM HOU DDP",
                inco=DDP,
                loc=HOU),

        Price(ticker=BZ,
                month=FMp1,
                desc="BZ FMp1 HOU DDP",
                inco=DDP,
                loc=HOU),

        Price(ticker=BZ,
                month=FMp2,
                desc="BZ FMp2 HOU DDP",
                inco=DDP,
                loc=HOU),

        Price(ticker=BZ,
                month=front_month,
                desc="BZ FM LMR DDP",
                inco=DDP,
                loc=LMR),

        Price(ticker=BZ,
                month=FMp1,
                desc="BZ FMp1 LMR DDP",
                inco=DDP,
                loc=LMR),

        Price(ticker=BZ,
                month=FMp2,
                desc="BZ FMp2 LMR DDP",
                inco=DDP,
                loc=LMR)
    ]

    return prices
