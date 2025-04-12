from app.models.board_plan import threshold, find_level


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

    
    
    
         
    
    @staticmethod
    def get_sales_details(user_id):
        """Get sales details including sales done, required for salary, and for next level."""

        sales_done = Sell.get_sales(user_id)
        if find_level(user_id) == 0:
            sales_needed_for_salary = -1
        else:
            sales_needed_for_salary = threshold(find_level(user_id)) - sales_done

        sales_needed_for_next_level = 6 - sales_done
        
        #get_name
        query = "SELECT name, level FROM users WHERE id = %s"
        values = (user_id,)
        cursor = mysql.connection.cursor()
        try:
            cursor.execute(query, values)
            row = cursor.fetchone()
            if row:
                name = row[0]
                level = row[1]
            else:
                name = None
                level = None
        except Exception as e:
            print(f"Error fetching user details: {e}")
            name = None
            level = None
        finally:
            cursor.close()



    

        return {
            "sales_done": sales_done,
            "sales_needed_for_salary": sales_needed_for_salary,
            "sales_needed_for_next_level": sales_needed_for_next_level,
            "name": name,
            "level": level+1,
        }