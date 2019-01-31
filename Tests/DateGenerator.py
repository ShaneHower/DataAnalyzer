import datetime
import random


class DateGenerator:
    def __init__(self):
        pass

    def generate(self):
        year = random.choice([2017, 2018])
        month = random.choice(range(1, 13))
        if month == 2:
            day = random.choice(range(1, 29))
        elif month in [4, 6, 9, 11]:
            day = random.choice(range(1, 31))
        else:
            day = random.choice(range(1, 32))
        return datetime.date(year, month, day)