from flask import Flask
import os
from src.routes import app as routes_app

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.getenv("FLASK_SECRET_KEY") or "braingainssecretkey"
app.register_blueprint(routes_app)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
