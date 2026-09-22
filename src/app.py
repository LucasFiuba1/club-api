from flask import Flask, jsonify

from src.routes.canchas.cancha_routes import cancha_routes
from src.utils.error_utils import build_error
from src.routes.socios.socio_routes import socio_routes


def create_app():
    app = Flask(__name__)

    app.register_blueprint(socio_routes)
    app.register_blueprint(cancha_routes)

    @app.errorhandler(500)
    def handle_internal_server_error(error):
        return (
            jsonify(
                build_error(
                    "ERROR_INTERNO",
                    "Error interno del servidor",
                    "Ocurrio un error interno en el servidor",
                )
            ),
            500,
        )
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
