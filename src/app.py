from flask import Flask

from routes.socios import socio_routes
from routes.canchas import cancha_routes
from routes.deportes import deporte_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(socio_routes)
    app.register_blueprint(cancha_routes)
    app.register_blueprint(deporte_routes)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
