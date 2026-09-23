from flask import Flask

from routes.socios.socio_routes import socio_routes
from routes.canchas.cancha_routes import cancha_routes
from routes.reservas.reserva_routes import reserva_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(socio_routes)
    app.register_blueprint(cancha_routes)
    app.register_blueprint(reserva_routes)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
