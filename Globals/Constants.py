from datetime import datetime

HOLIDAYS_2021 = [datetime(2021, 1, 1), datetime(2021, 1, 18), datetime(2021, 2, 15),
            datetime(2021, 4, 2),datetime(2021, 5, 31), datetime(2021, 7, 5),
            datetime(2021,9, 6),datetime(2021,11, 25), datetime(2021,12, 24)]

HOLIDAYS = [datetime(2022, 1, 17), datetime(2022, 2, 21), datetime(2022, 4, 15),datetime(2022, 5, 30),
            datetime(2022, 6, 20),datetime(2022, 7, 4), datetime(2022, 9, 5),
            datetime(2022,11, 24),datetime(2022,12, 26)]

HOLIDAYS.extend(HOLIDAYS_2021)