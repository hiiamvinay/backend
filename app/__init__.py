from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS

from app.routes.auth import auth_bp, init_auth_blueprint
from app.routes.sells import sell_bp, init_sell_blueprint
from app.routes.admin import admin_bp, init_admin_blueprint
from app.routes.koupean import koupean_bp, init_koupean_blueprint
from app.routes.board import board_bp, init_board_blueprint

from app.models.users import init_model_user
from app.models.sells import init_model_sell
from app.models.koupean import init_model_koupean

from app.config import Config


mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    

    mysql.init_app(app)


    init_auth_blueprint(mysql)
    init_sell_blueprint(mysql)
    init_admin_blueprint(mysql)
    init_koupean_blueprint(mysql)
    init_board_blueprint(mysql)


    init_model_user(mysql)
    init_model_sell(mysql)
    init_model_koupean(mysql)
    
    

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(sell_bp, url_prefix='/sell')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(koupean_bp, url_prefix='/koupean')
    app.register_blueprint(board_bp, url_prefix='/board')
    


    return app



    
   

