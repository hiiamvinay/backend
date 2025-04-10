mysql = None

def init_model_sell(mysql_instance):
    global mysql
    mysql = mysql_instance

class Sell:
    @staticmethod
    def add_sale(user_id, quantity):
        """Insert a new sale record (tracks number of sales)."""
        query = "INSERT INTO sales (user_id, quantity) VALUES (%s, %s)"
        values = (user_id, quantity)

        cursor = mysql.connection.cursor()
        try:
            cursor.execute(query, values)
            mysql.connection.commit()
            return {"message": "Sale recorded successfully!"}
        except Exception as e:
            mysql.connection.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def get_sales(user_id):
        """Fetch total number of sales done by a user for the current month."""
        query = """
        SELECT COALESCE(SUM(quantity), 0) 
        FROM sales 
        WHERE user_id = %s 
        AND MONTH(date) = MONTH(CURRENT_DATE()) 
        AND YEAR(date) = YEAR(CURRENT_DATE());
        """
        cursor = mysql.connection.cursor()
        try:
            cursor.execute(query, (user_id,))
            total_sales = cursor.fetchone()[0]
            return total_sales
        finally:
            cursor.close()

    def mini_id():
        query = """SELECT MIN(id) FROM users """
        cursor = mysql.connection.cursor()
        try:
            cursor.execute(query)
            min_id = cursor.fetchone()[0]
            return min_id
        finally:
            cursor.close()
    
    
         
    
    @staticmethod
    def get_sales_details(user_id, salary_threshold=-1, next_level_threshold=7):
        """Get sales details including sales done, required for salary, and for next level."""
        sales_done = Sell.get_sales(user_id)
        sales_needed_for_next_level = max(0, next_level_threshold - sales_done)
        sales_needed_for_salary=-1
    

        return {
            "sales_done": sales_done,
            "sales_needed_for_salary": sales_needed_for_salary,
            "sales_needed_for_next_level": sales_needed_for_next_level
        }