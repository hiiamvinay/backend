from app.models.koupean import get_all_koupeans, add_koupean, delete_koupean_by_code
from app.services.koupean import generate_koupeans
from flask import Blueprint, request, jsonify


mysql = None

def init_koupean_blueprint(mysql_instance):
    global mysql
    mysql = mysql_instance

koupean_bp = Blueprint("koupean", __name__)

@koupean_bp.route("/add_koupean", methods=["POST"])
def add_koupean_route():
    data = request.get_json()
    number = data.get("number")

    if not number:
        return jsonify({"error": "Missing required number"}), 400

    list_of_koupean = generate_koupeans(number)

    for i in list_of_koupean:
        add_koupean(i)
    
    return jsonify({"message": "Koupean code added successfully"}), 201

@koupean_bp.route("/get_koupeans", methods=["GET"])
def get_koupeans_route():
    """Get all koupean codes."""
    koupeans = get_all_koupeans()
    return jsonify(koupeans), 200

@koupean_bp.route("/delete_koupean", methods=["DELETE"])
def delete_koupean_route():
    """Delete a koupean code by code."""
    data = request.get_json()
    code = data.get("code")

    if not code:
        return jsonify({"error": "Missing required code"}), 400

    result = delete_koupean_by_code(code)
    
    return jsonify({"message": "Koupean code deleted successfully"}), 200
    