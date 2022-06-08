from datetime import timedelta


def average_time_between_list_datetimes(list_of_dates):
    list_of_dates.sort(reverse=True)
    # subtracting datetimes gives timedeltas
    timedeltas = [list_of_dates[i - 1] - list_of_dates[i] for i in range(1, len(list_of_dates))]

    # giving datetime.timedelta(0) as the start value makes sum work on tds
    return sum(timedeltas, timedelta(0)) / len(timedeltas)
