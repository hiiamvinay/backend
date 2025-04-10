from flask import Blueprint, request, jsonify
from app.models.sells import Sell
from app.models.koupean import verify_koupean, delete_koupean_by_code


mysql = None 

def init_sell_blueprint(mysql_instance):
    global mysql
    mysql = mysql_instance



sell_bp = Blueprint('sell', __name__)

@sell_bp.route('/sales/<int:user_id>', methods=['GET'])
def get_sales(user_id):
    """API to get sales details for a user."""
    sales_data = Sell.get_sales_details(user_id)
    return jsonify(sales_data)

@sell_bp.route('/sales', methods=['POST'])
def add_sale():
    """API to record a sale."""
    data = request.json
    user_id = data.get("user_id")
    quantity = data.get("quantity")  # Track number of sales

    if not user_id or not quantity:
        return jsonify({"error": "Missing user_id or quantity"}), 400

    response = Sell.add_sale(user_id, quantity)

  

    return jsonify(response)

@sell_bp.route('/kounen-payment', methods=['POST'])
def kounen_payment():
    """API to record a kounen payment."""
    data = request.json
    user_id = data.get("user_id")
    code = data.get("kounen_code")

    if not user_id or not code:
        return jsonify({"error": "Missing user_id or kounen_code"}), 400
    
    if not verify_koupean(code):
        return jsonify({"error": "Invalid kounen code"}), 400
    else:
        Sell.add_sale(user_id, 1)
        delete_koupean_by_code(str(code))
        return jsonify({"message": "sale is successfully"}), 200
    return jsonify({"message": "sale is successfully"}), 200