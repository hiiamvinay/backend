from datetime import datetime

# This will be set when the model is initialized
mysql = None

def init_model_koupean(mysql_instance):
    global mysql
    mysql = mysql_instance

def add_koupean(code):
    """Add a new koupean code."""
    query = "INSERT INTO koupean_codes (koupean_code) VALUES (%s)"
    values = (code,)
    
    connection = mysql.connection
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
    finally:
        cursor.close()

def delete_koupean_by_code(code):
    """Delete a koupean code by its value."""
    query = "DELETE FROM koupean_codes WHERE koupean_code = %s"
    values = (code,)

    connection = mysql.connection
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
    finally:
        cursor.close()

def get_all_koupeans():
    """Retrieve all koupean codes."""
    query = "SELECT * FROM koupean_codes"

    connection = mysql.connection
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        # Optionally convert results to a list of dicts manually:
        koupeans = [{"id": row[0], "koupean_code": row[1]} for row in results]
        return koupeans
    finally:
        cursor.close()
        
def verify_koupean(code):
    """Check if a koupean code exists in the database."""
    query = "SELECT COUNT(*) FROM koupean_codes WHERE koupean_code = %s"
    values = (code,)

    connection = mysql.connection
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        result = cursor.fetchone()
        return result[0] > 0  # True if the code exists, False otherwise
    finally:
        cursor.close()