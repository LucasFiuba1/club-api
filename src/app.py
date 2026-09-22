from flask import Flask

from routes.reservas.reservas_routes import reserva_bp
from routes.socios.socio_routes import socio_routes


def create_app():
    app = Flask(__name__)
    app.register_blueprint(socio_routes)
    app.register_blueprint(reserva_bp)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
