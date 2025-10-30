from app.db import get_db_connection

def log_operation(user_id, operation, operation_id, custom_desc=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO t_operation_log (user_id, operation_type, operation_desc, operation_time, operation_id) 
                VALUES (%s, %s, %s, NOW(), %s)
            """
            operation_type = operation['type']
            operation_desc = custom_desc if custom_desc else operation.get('desc', '未提供描述')
            cursor.execute(sql, (user_id, operation_type, operation_desc, operation_id))
        conn.commit()
    except Exception as e:
        print(f"Error logging operation: {e}")
    finally:
        conn.close()
