from typing import List

import requests
from circuitbreaker import circuit
from requests import RequestException, HTTPError

from source.custom_exceptions.custom_exception import NotValidGithubURL
from source.utils.logging import logger
import aiohttp

class GithubApiConnector:
    def __init__(self, access_token: str):
        # we need to login in order to collect private data
        self.headers = {'Authorization': f"token {access_token}"}

    @circuit(failure_threshold=10, expected_exception=RequestException, recovery_timeout=10)
    async def handle_api_response(self, url: str) -> List[dict]:
        async with aiohttp.ClientSession() as session:
            page = 1
            pagination_query = f'?per_page=100&page={page}'
            try:
                async with session.get(url + pagination_query, headers=self.headers) as api_response:
                    response = []
                    api_response.raise_for_status()
                    status = api_response.status
                    api_response_json = await api_response.json()
                    response.append(api_response_json)
                while status == 200:
                    page += 1
                    pagination_query = f'?per_page=100&page={page}'
                    async with session.get(url + pagination_query, headers=self.headers) as api_response:
                        status = api_response.status
                        if status == 200:
                            response.append(await api_response.json())
                return response
            except HTTPError as e:
                logger.error(e)
                raise NotValidGithubURL
