from app.db import get_db_connection


# 获取账号列表
def get_accounts():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT account.*,t_role.role_name FROM 
                (
                SELECT t_account.*,t_user_roles.role_id  FROM t_account
                LEFT JOIN t_user_roles ON t_user_roles.user_id = t_account.id
                ) as account
                LEFT JOIN t_role ON t_role.role_id = account.role_id
            '''
            cursor.execute(sql)
            accounts = cursor.fetchall()
            return accounts
    except Exception as e:
        print(f"Error get_accounts: {e}")
    finally:
        conn.close()

#查询账号信息
def get_user(user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT account.*,t_role.role_name FROM 
                (
                SELECT t_account.*,t_user_roles.role_id  FROM t_account
                LEFT JOIN t_user_roles ON t_user_roles.user_id = t_account.id
                ) as account
                LEFT JOIN t_role ON t_role.role_id = account.role_id
                WHERE account.id = %s
            '''
            cursor.execute(sql, user_id)
            user = cursor.fetchone()
            return user
    except Exception as e:
        print(f"Error get_user: {e}")
    finally:
        conn.close()

#更新账号角色
def update_user_role(user_id,role_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                UPDATE t_user_roles 
                SET role_id = %s
                WHERE user_id = %s
            '''
            cursor.execute(sql, (role_id, user_id))
            conn.commit()
            # 获取插入记录的ID
            return cursor.lastrowid
    except Exception as e:
        print(f"Error update_user_role: {e}")
    finally:
        conn.close()

#更新账号密码
def update_user_password(user_id,password):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                UPDATE t_account 
                SET password = %s
                WHERE id = %s
            '''
            cursor.execute(sql, (password, user_id))
            conn.commit()
            # 获取插入记录的ID
            return cursor.lastrowid
    except Exception as e:
        print(f"Error update_user_password: {e}")
    finally:
        conn.close()

# 添加账号
def add_user(username, password, realname, phone, email):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                INSERT INTO t_account (username, password, realname, phone, email)
                VALUES (%s, %s, %s, %s, %s)
            '''
            cursor.execute(sql, (username, password, realname, phone, email))
            conn.commit()
            # 获取插入记录的ID
            return cursor.lastrowid
    except Exception as e:
        print(f"Error add_user: {e}")
    finally:
        conn.close()


# 删除账号
def delete_user(userid):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                DELETE FROM t_account 
                WHERE id = %s
            '''
            cursor.execute(sql, userid)
            conn.commit()
    except Exception as e:
        print(f"Error delete_user: {e}")
    finally:
        conn.close()


# 获取用户权限
def has_permission(user_id, permission_name):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT COUNT(1) as c
                FROM t_user_roles  ur
                JOIN t_role_permissions rp ON ur.role_id = rp.role_id
                JOIN t_permissions p ON rp.permission_id = p.permission_id
                WHERE ur.user_id = %s AND p.permission_name = %s
            """
            cursor.execute(sql, (user_id, permission_name))
            result = cursor.fetchone()
            return result['c'] > 0
    except Exception as e:
        print(f"Error in has_permission: {e}")
        return False
    finally:
        conn.close()

# 获取用户权限
def has_permission_show(user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            permissions_list = []
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """
                    SELECT permission_name
                    FROM t_user_roles  ur
                    JOIN t_role_permissions rp ON ur.role_id = rp.role_id
                    JOIN t_permissions p ON rp.permission_id = p.permission_id
                    WHERE ur.user_id = %s
                """
            cursor.execute(sql, (user_id,))
            permissions = cursor.fetchall()

            for permission in permissions:
                try:
                    permissions_list.append(permission['permission_name'])  # 假设是字典
                    print(permissions_list)
                except KeyError:  # 如果既不是元组也不是预期的字典结构
                    print(f"Unexpected item format in permissions: {permission}")
            return permissions_list
    except Exception as e:
        print(f"Error in has_permission: {e}")
        return False
    finally:
        conn.close()
