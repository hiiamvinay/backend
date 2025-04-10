from flask import Blueprint, request, jsonify
from app.models.users import create_user, get_user_id, update_password, is_phone_number_exists
from app.services.phonenumber import send_otp

mysql = None 
temp_userdata = dict()
temp_reset_data = {}

def init_auth_blueprint(mysql_instance):
    global mysql
    mysql = mysql_instance

auth_bp = Blueprint("auth", __name__)




@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    phone_number = data.get("phone_number")
    password = data.get("password")


    if not name or not phone_number or not password:
        return jsonify({"error": "Missing required information"}), 400
    
    if is_phone_number_exists(phone_number):
        return jsonify({"error": "Phone number already exists"}), 400
    
    otp = send_otp(phone_number)
    temp_userdata[phone_number] = {"name": name, "password": password, "otp": otp}
    
    return jsonify({"message": "otp send successfully"}), 200

@auth_bp.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    phone_number = data.get("phone_number")
    otp = data.get("otp")
    
    if not phone_number or not otp:
        return jsonify({"error": "Missing required information"}), 400
    
    if phone_number not in temp_userdata:
        return jsonify({"error": "Phone number not found"}), 404
    
    if temp_userdata[phone_number]["otp"] != otp:
        return jsonify({"error": "Invalid OTP"}), 400
    
    create_user(temp_userdata[phone_number]["name"], phone_number, temp_userdata[phone_number]["password"])
    del temp_userdata[phone_number]
    return jsonify({"message": "User created successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    phone_number = data.get("phone_number")
    password = data.get("password")
    
    if not phone_number or not password:
        return jsonify({"error": "Missing required information"}), 400
    
    user_id = get_user_id(phone_number, password)
    if user_id:
        return jsonify({"user_id": user_id}), 200
    return jsonify({"error": "Invalid phone number or password"}), 400


@auth_bp.route("/reset", methods=["POST"])
def reset_request():

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input. Please provide JSON data."}), 400

    phone_number = data.get("phone_number")
    new_password = data.get("new_password")

    if not phone_number or not new_password:
        return jsonify({"error": "Missing required information"}), 400

    if not is_phone_number_exists(phone_number):
        return jsonify({"error": "Phone number is not registered"}), 404

    # Generate and send OTP to user
    otp = send_otp(phone_number)
    temp_reset_data[phone_number] = {"otp": otp, "new_password": new_password}

    return jsonify({"message": "OTP sent successfully"}), 200


@auth_bp.route("/verify_reset_otp", methods=["POST"])
def verify_reset_otp():
    """
    Step 2: Verify OTP and reset password.
    - User provides phone number and OTP.
    - If OTP matches, update the password.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input. Please provide JSON data."}), 400

    phone_number = data.get("phone_number")
    otp = data.get("otp")

    if not phone_number or not otp:
        return jsonify({"error": "Missing required information"}), 400

    if phone_number not in temp_reset_data:
        return jsonify({"error": "No reset request found for this number"}), 404

    # Convert otp to int for comparison
    try:
        otp_int = int(otp)
    except ValueError:
        return jsonify({"error": "OTP must be a number"}), 400

    if temp_reset_data[phone_number]["otp"] != otp_int:
        return jsonify({"error": "Invalid OTP"}), 400

    # Update the password in the database
    new_password = temp_reset_data[phone_number]["new_password"]
    update_password(phone_number, new_password)

    # Remove temporary data after successful password reset
    del temp_reset_data[phone_number]

    return jsonify({"message": "Password reset successfully"}), 200
