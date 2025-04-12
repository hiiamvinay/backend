

mysql = None


def init_model_board(mysql_instance):
    global mysql
    mysql = mysql_instance


def threshold(level):
    match level:
        case 0:
            return 0
        case 1:
            return 3
        case 2:
            return 6
        case 3:
            return 12
        case 4:
            return 24
        case 5:
            return 48
        case 6:
            return 84
        case 7:
            return 168
        case 8:
            return 336
        case 9:
            return 672
        case 10:
            return 1400
        

def find_level(id):
    # GET LEVEL
    query = "SELECT level FROM users WHERE id = %s"
    values = (id,)
    cursor = mysql.connection.cursor()
    try:
        cursor.execute(query, values)
        level = cursor.fetchone()[0]
        return level
    except Exception as e:
        print(f"Error fetching user level: {e}")
        return None
    finally:
        cursor.close()


def get_parent_id(userid):
    query = "SELECT parent_id FROM users WHERE id = %s"
    values = (userid,)
    cursor = mysql.connection.cursor()
    try:    
        cursor.execute(query, values)
        parent_id = cursor.fetchone()[0]
        return parent_id  
    except Exception as e:
        print(f"Error fetching parent ID: {e}")
        return None
    finally:    
        cursor.close()


def child_counts(userid, level):
    query = "SELECT COUNT(*) FROM users WHERE parent_id = %s AND level = %s"
    values = (userid,level)
    cursor = mysql.connection.cursor()
    try:
        cursor.execute(query, values)
        child_count = cursor.fetchone()[0]
        return child_count
    except Exception as e:
        print(f"Error fetching child count: {e}")
        return None
    finally:
        cursor.close()





def board(userid):
    from app.models.sells import Sell
    
    level = find_level(userid)
    child_count = child_counts(userid, level)


    if child_count > 5 and Sell.get_sales(userid) >= threshold(level):
        query="UPDATE users SET level = level + 1 WHERE id = %s"
        values = (userid,)
        cursor = mysql.connection.cursor()
        try:
            cursor.execute(query, values)
            mysql.connection.commit()
        except Exception as e:
            print(f"Error updating user level: {e}")
            mysql.connection.rollback()
        finally:
            cursor.close()
    
    
    parent_id = get_parent_id(userid)
    if parent_id is None:
        return None
    
    parent_level = find_level(parent_id)
    parent_child_count = child_counts(parent_id, parent_level)
    
    sales = Sell.get_sales(parent_id) or 0  # Default to 0 if None
    if parent_child_count + child_count > 5 and sales >= threshold(parent_level):

        query="UPDATE users SET level = level + 1 WHERE id = %s"
        values = (parent_id,)
        cursor = mysql.connection.cursor()
        try:
            cursor.execute(query, values)
            mysql.connection.commit()
        except Exception as e:
            print(f"Error updating parent level: {e}")
            mysql.connection.rollback()
        finally:
            cursor.close()


    
    
