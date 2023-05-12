from flask import Flask, render_template, abort
from flask_caching import Cache
import requests


app = Flask(__name__)
app.config.from_prefixed_env()
app_config = {
    "CACHE_TYPE": app.config.get("CACHE_TYPE", "SimpleCache"),
    "CACHE_DEFAULT_TIMEOUT": app.config.get("CACHE_DEFAULT_TIMEOUT", 300),
}
if app_config.get("CACHE_TYPE") == "RedisCache":
    app_config.update(
        {
            "CACHE_REDIS_HOST": app.config.get("CACHE_REDIS_HOST"),
            "CACHE_REDIS_DB": app.config.get("CACHE_REDIS_DB"),
        }
    )
app.config.from_mapping(app_config)

cache = Cache(app)

LIST_TYPES = ("emailed", "shared", "viewed")
API_URI = "https://api.nytimes.com/svc/mostpopular/v2/"


def fetch_most_popular(list_type, period=1):
    url = f"{API_URI}{list_type}/{period}.json?api-key={app.config.get('NYT_API_KEY')}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


@app.get("/")
def index():
    return render_template("base.html", list_types=LIST_TYPES)


@app.get("/most-popular/<list_type>")
@cache.cached()
def render_most_popular(list_type=None):
    if not list_type or list_type not in LIST_TYPES:
        abort(404)
    data = fetch_most_popular(list_type)
    context = {
        "list_types": LIST_TYPES,
        "list_type": list_type,
        "articles": data.get("results"),
    }
    return render_template("most_popular.html", **context)
