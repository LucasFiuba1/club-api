from flask import Flask
from routes.canchas.cancha_routes import cancha_routes

app = Flask(__name__)
app.register_blueprint(cancha_routes)

@app.get("/")
def home():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True, port=5001)