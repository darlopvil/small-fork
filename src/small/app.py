from flask import Flask

from os import environ

from .const import Config
from .views import home, article, error, proxy


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(home.bp)
    app.register_blueprint(article.bp)
    app.register_blueprint(error.bp)
    app.register_blueprint(proxy.bp)

    return app


def main():
    app = create_app()
    port = int(environ.get("PORT", 8115))
    app.run(port=port)


if __name__ == "__main__":
    main()
