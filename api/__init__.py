from flask import Flask
from flask_restx import Api
from .orders.views import order_namespace
from .auth.views import auth_namespace
from .config.config import config_dict
from .utils import db
from .models.orders import Order
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed

# set FLASK_APP=api/
# flask shell, db, User, Order, db.create_all()
# echo $FLASK_APP

def create_app(config = config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    api = Api(app, title= 'Pizza Delivery API')

    api.add_namespace(order_namespace)
    api.add_namespace(auth_namespace, path='/auth')

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404


    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method not allowed"}, 404

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'User':User,
            'Order': Order
        }


    return app

    