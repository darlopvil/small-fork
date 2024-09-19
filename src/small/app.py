from flask import Flask

from os import environ

from .views import home, article, error, proxy


def create_app():
    app = Flask(__name__)

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
