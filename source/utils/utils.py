from datetime import timedelta, datetime
from typing import List, Dict


def average_time_between_list_datetimes(list_of_dates):
    list_of_dates.sort(reverse=True)
    # subtracting datetimes gives timedeltas
    timedeltas = [list_of_dates[i - 1] - list_of_dates[i] for i in range(1, len(list_of_dates))]

    # giving datetime.timedelta(0) as the start value makes sum work on tds
    return sum(timedeltas, timedelta(0)) / len(timedeltas)


def count_days_from_list_datetimes(list_of_dates: List[datetime]) -> dict:
    """
    count days from list of dates
    input:
        list_of_dates: List[datetime]
    output: Dict[datetime, int]
    """
    days_count = {}
    for date in list_of_dates:
        day = str(date.date())
        if day in days_count.keys():
            days_count[day] += 1
        else:
            days_count[day] = 1
    return days_count
