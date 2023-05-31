from flask import Flask
from apis import blueprint
from apis.models import db

app = Flask(__name__)
app.register_blueprint(blueprint, url_prefix='/api')
app.config.from_object('api.apis.config.BaseConfig')
db.init_app(app)

