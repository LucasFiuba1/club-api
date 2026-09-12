from flask import Flask

from routes.socios import socio_routes


def create_app():
    app = Flask(__name__)
    app.register_blueprint(socio_routes)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)