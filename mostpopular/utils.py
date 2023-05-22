import requests

from mostpopular.constants import API_URI

def fetch_most_popular(api_key, list_type, period=1):
    url = f"{API_URI}{list_type}/{period}.json?api-key={api_key}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()
