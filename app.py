from flask import Flask
from src.routes import app as routes_app

app = Flask(__name__, template_folder='templates', static_folder='static')
app.register_blueprint(routes_app)

if __name__ == "__main__":
    app.run()
