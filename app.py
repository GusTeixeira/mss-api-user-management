from flask import Flask
from config import Config
from flask_cors import CORS
from api.routes.user_routes import auth
from api.databases.config import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True)