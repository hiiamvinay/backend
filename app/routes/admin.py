
from flask import Blueprint, request, jsonify


mysql = None 


def init_admin_blueprint(mysql_instance):
    global mysql
    mysql = mysql_instance

admin_bp = Blueprint("admin", __name__)

@admin_bp.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing required information"}), 400

    if username == "admin" and password == "adminlog@success":
        return jsonify({"message": "Login successful", "adminId" : "admin_user12"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    
    

