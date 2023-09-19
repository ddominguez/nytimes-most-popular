from typing import Any

import requests

from mostpopular.constants import API_URI
from mostpopular.extensions import cache


def fetch_most_popular(api_key: str, list_type: str, period: int = 1) -> Any:
    cache_key = f"{list_type}:{period}"
    if cache.has(cache_key):
        return cache.get(cache_key)

    url = f"{API_URI}{list_type}/{period}.json?api-key={api_key}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    cache.set(cache_key, data)
    return data
