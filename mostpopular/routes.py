from flask import Blueprint, abort, current_app, render_template

from mostpopular.constants import LIST_TYPES
from mostpopular.extensions import cache
from mostpopular.utils import fetch_most_popular

nyt_app = Blueprint("nyt_app", __name__, template_folder="templates")


@nyt_app.get("/")
def index():
    return render_template("base.html", list_types=LIST_TYPES)


@nyt_app.get("/most-popular/<list_type>")
@cache.cached()
def render_most_popular(list_type=None):
    if list_type not in LIST_TYPES:
        abort(404)
    data = fetch_most_popular(current_app.config.get('NYT_API_KEY'), list_type)
    context = {
        "list_types": LIST_TYPES,
        "list_type": list_type,
        "articles": data.get("results"),
    }
    return render_template("most_popular.html", **context)
