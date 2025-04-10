from flask import Blueprint, request
from app.models.sells import Sell

mysql = None 


def init_board_blueprint(mysql_instance):
    global mysql
    mysql = mysql_instance

board_bp = Blueprint("board", __name__)

@board_bp.route('/get_board', methods=["GET"])
def get_board():
    min_id = Sell.mini_id()
    query = """SELECT COUNT(*) FROM users"""
    cursor = mysql.connection.cursor()
    try:
        cursor.execute(query)
        count = cursor.fetchone()[0]
        if count >= 7:
            return {"message": "Board is full", "min_id": int(min_id)}, 200
        else:
            return {"message": "Board is not full, board is broken"}, 200
    finally:
        cursor.close()

@board_bp.route('/board_count', methods=["GET"])
def board_count():
    query = """SELECT COUNT(*) FROM users"""
    cursor = mysql.connection.cursor()
    try:
        cursor.execute(query)
        count = cursor.fetchone()[0]
        return {"user_count": count}, 200
    finally:
        cursor.close()