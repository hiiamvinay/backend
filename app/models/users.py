from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# This will be set when the model is initialized
mysql = None

def init_model_user(mysql_instance):
    global mysql
    mysql = mysql_instance

def create_user(name, phone_number, password, parent_id=0):
    """Create a new user."""
    hashed_password = generate_password_hash(password)
    query = "INSERT INTO users (name, phone_number, password, parent_id) VALUES (%s, %s, %s, %s)"
    values = (name, phone_number, hashed_password, parent_id)

    connection = mysql.connection  # Corrected database connection
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
    finally:
        cursor.close()

def get_user_id(phone_number, password):
    """Get user ID by verifying phone number and password."""
    query = "SELECT id, password FROM users WHERE phone_number = %s"
    values = (phone_number,)

    connection = mysql.connection  # Corrected database connection
    cursor = connection.cursor()    # Use default tuple-based cursor
    try:
        cursor.execute(query, values)
        user = cursor.fetchone()
        # Accessing tuple elements by index: user[0] is id, user[1] is password.
        if user and check_password_hash(user[1], password):
            return user[0]
        return None
    finally:
        cursor.close()


def update_password(phone_number, new_password):
    """Update the password for a user."""
    hashed_password = generate_password_hash(new_password)
    query = "UPDATE users SET password = %s WHERE phone_number = %s"
    values = (hashed_password, phone_number)

    connection = mysql.connection  # Corrected database connection
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        return cursor.rowcount > 0  # Return True if a row was updated
    finally:
        cursor.close()

def reset_password(phone_number, name, new_password):
    """Reset password by verifying phone number and name."""
    hashed_password = generate_password_hash(new_password)
    query = "UPDATE users SET password = %s WHERE phone_number = %s AND name = %s"
    values = (hashed_password, phone_number, name)

    connection = mysql.connection  # Corrected database connection
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        return cursor.rowcount > 0  # Return True if a row was updated
    finally:
        cursor.close()

def is_phone_number_exists(phone_number):
    """Check if a phone number already exists in the users table."""
    query = "SELECT COUNT(*) FROM users WHERE phone_number = %s"
    
    # Get connection from the framework (e.g., Flask-MySQLdb)
    connection = mysql.connection
    cursor = connection.cursor()
    
    try:
        cursor.execute(query, (phone_number,))
        result = cursor.fetchone()
        return result[0] > 0  # Using tuple indexing
    finally:
        cursor.close()
        # Remove manual connection close if the framework manages it.
        # connection.close()
