import unittest
from unittest import mock, IsolatedAsyncioTestCase

import pytest as pytest

from source.services.github_activity_service import GithubActivityService
from source.services.github_connector import GithubApiConnector
from tests import mock_response


class TestServices(unittest.TestCase):
    github_api_connector = mock.Mock(spec=GithubApiConnector)
    github_api_connector.handle_api_response.return_value = mock_response

    async def test_github_activity_service(self):
        github_activity_service = GithubActivityService(api_service=self.github_api_connector)
        response = await github_activity_service.get_events(owner='youssefkhammassi', repo='github_activity_analysis_service')
        self.assertEqual(response.repository, 'github_activity_analysis_service')
        self.assertEqual(response.owner, 'youssefkhammassi')
        self.assertEqual(len(response.activity), 2)
        self.assertEqual(response.activity[0].type, 'PushEvent')
        self.assertEqual(response.activity[1].type, 'PullRequestEvent')

    async def test_github_activity_service_pull_requests(self):
        github_activity_service = GithubActivityService(api_service=self.github_api_connector)
        response = await github_activity_service.get_pull_events(owner='youssefkhammassi', repo='github_activity_analysis_service')
        self.assertEqual(response.repository, 'github_activity_analysis_service')
        self.assertEqual(response.owner, 'youssefkhammassi')
        self.assertEqual(response.average_duration_between_pulls, '0:00:00')
        self.assertEqual(len(response.activity), 1)
        self.assertEqual(response.activity[0].type, 'PullRequestEvent')

    async def test_github_activity_service_watch_events(self):
        github_activity_service = GithubActivityService(api_service=self.github_api_connector)
        response = await github_activity_service.get_watch_events(owner='youssefkhammassi', repo='github_activity_analysis_service')
        self.assertEqual(response.repository, 'github_activity_analysis_service')
        self.assertEqual(response.owner, 'youssefkhammassi')
        self.assertEqual(len(response.activity), 0)
        self.assertEqual(response.activity, [])

    async def test_github_activity_service_issues_events(self):
        github_activity_service = GithubActivityService(api_service=self.github_api_connector)
        response = await github_activity_service.get_issues_events(owner='youssefkhammassi', repo='github_activity_analysis_service')
        self.assertEqual(response.repository, 'github_activity_analysis_service')
        self.assertEqual(response.owner, 'youssefkhammassi')
        self.assertEqual(len(response.activity), 0)
        self.assertEqual(response.activity, [])

    async def test_get_events_grouped_by_day(self):
        github_activity_service = GithubActivityService(api_service=self.github_api_connector)
        response = await github_activity_service.get_events_grouped(owner='youssefkhammassi', repo='github_activity_analysis_service', offset=None)
        self.assertEqual(response.repository, 'github_activity_analysis_service')
        self.assertEqual(response.owner, 'youssefkhammassi')
        self.assertEqual(len(response.activity.PullRequestEvent), 1)
        self.assertEqual(response.activity.PullRequestEvent[0].type, 'PullRequestEvent')
        self.assertEqual(len(response.activity.IssuesEvent), 0)
        self.assertEqual(response.activity.IssuesEvent, [])
        self.assertEqual(len(response.activity.WatchEvent), 0)
        self.assertEqual(response.activity.WatchEvent, [])

    async def test_get_events_grouped_by_day_with_offset(self):
        github_activity_service = GithubActivityService(api_service=self.github_api_connector)
        response = await github_activity_service.get_events_grouped(owner='youssefkhammassi', repo='github_activity_analysis_service', offset=1)
        self.assertEqual(response.repository, 'github_activity_analysis_service')
        self.assertEqual(response.owner, 'youssefkhammassi')
        self.assertEqual(len(response.activity.PullRequestEvent), 0)
        self.assertEqual(response.activity.PullRequestEvent, [])
        self.assertEqual(len(response.activity.IssuesEvent), 0)

    async def test_get_number_of_pull_events_per_day(self):
        github_activity_service = GithubActivityService(api_service=self.github_api_connector)
        response = await github_activity_service.get_number_of_pull_events_per_day(owner='youssefkhammassi', repo='github_activity_analysis_service')
        self.assertEqual(type(response), dict)
        self.assertEqual(response.get('2022-06-08'), 1)
