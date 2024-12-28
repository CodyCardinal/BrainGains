from flask import Flask
import os
from src.routes import bp as routes_bp
from src.functions import db_cli
from src.functions import jinja_filter_days_ago

app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = os.getenv("FLASK_SECRET_KEY") or "braingainssecretkey"
app.register_blueprint(routes_bp)
app.cli.add_command(db_cli)

with app.app_context():
    app.jinja_env.filters['days_ago'] = jinja_filter_days_ago

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)