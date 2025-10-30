from app.db import get_db_connection


def get_flow_todo(type, status):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT todo_user_id FROM t_flow
                WHERE type = %s and status = %s
            """
            cursor.execute(sql, (type, status))
            row = cursor.fetchone()
            return None if row is None else row['todo_user_id']
    #except Exception as e:
    #    print(f"Error get_flow_todo: {e}")
    finally:
        conn.close()
