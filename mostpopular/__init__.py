from flask import Flask

from mostpopular.extensions import cache
from mostpopular.routes import nyt_app


def create_app(config={}):
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app_config = {
        "CACHE_TYPE": app.config.get("CACHE_TYPE", "NullCache"),
    }

    if config:
        app_config.update(config)

    if app_config.get("CACHE_TYPE") == "RedisCache":
        app_config.update(
            {
                "CACHE_DEFAULT_TIMEOUT": app.config.get("CACHE_DEFAULT_TIMEOUT", 300),
                "CACHE_REDIS_HOST": app.config.get("CACHE_REDIS_HOST"),
                "CACHE_REDIS_DB": app.config.get("CACHE_REDIS_DB"),
            }
        )

    app.config.from_mapping(app_config)
    app.register_blueprint(nyt_app)
    cache.init_app(app)

    return app
