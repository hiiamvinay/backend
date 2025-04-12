from flask import Blueprint, request, jsonify
from app.models.sells import Sell
from app.models.koupean import verify_koupean, delete_koupean_by_code
from app.models.users import create_user, is_phone_number_exists
from app.models.board_plan import board
from app.services.random_pass import random_password


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
    data = request.get_json()
    user_id = data.get('user_id')
    kounen_code = data.get('kounen_code')
    buyer_name = data.get('buyer_name')
    buyer_phone = data.get('buyer_phone')


    if not user_id or not kounen_code or not buyer_name or not buyer_phone:
        return jsonify({"error": "Missing user_id or kounen_code"}), 400
    
    if not verify_koupean(kounen_code):
        return jsonify({"error": "Invalid kounen code"}), 400
    else:
        Sell.add_sale(user_id, 1)
        if is_phone_number_exists(buyer_phone):
            delete_koupean_by_code(str(kounen_code))
            return jsonify({"message": "sale is successfully"}), 200
        else:  
            create_user(buyer_name,buyer_phone, random_password(), parent_id=user_id)
            board(userid=user_id)
            delete_koupean_by_code(str(kounen_code))
            return jsonify({"message": "sale is successfully"}), 200
    return jsonify({"error": "Failed to record sale"}), 500 