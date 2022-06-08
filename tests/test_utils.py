import unittest
from datetime import timedelta, datetime

from source.utils.utils import average_time_between_list_datetimes, count_days_from_list_datetimes
from source.utils.url_generator import generate_github_events_url


class TestUtils(unittest.TestCase):
    def test_average_time_between_list_datetimes(self):
        list_of_dates = [
            datetime(2019, 1, 1),
            datetime(2019, 1, 2),
            datetime(2019, 1, 3),
            datetime(2019, 1, 4),
            datetime(2019, 1, 5),
            datetime(2019, 1, 6)]
        self.assertEqual(average_time_between_list_datetimes(list_of_dates), timedelta(days=1))

    def test_count_days_from_list_datetimes(self):
        list_of_dates = [
            datetime(2019, 1, 1),
            datetime(2019, 1, 2),
            datetime(2019, 1, 3),
            datetime(2019, 1, 4),
            datetime(2019, 1, 5),
            datetime(2019, 1, 6)]
        self.assertEqual(count_days_from_list_datetimes(list_of_dates), {
            '2019-01-01': 1,
            '2019-01-02': 1,
            '2019-01-03': 1,
            '2019-01-04': 1,
            '2019-01-05': 1,
            '2019-01-06': 1})

    def test_generate_github_events_url(self):
        self.assertEqual(generate_github_events_url('repo', 'owner'), 'https://api.github.com/repos/owner/repo/events')



