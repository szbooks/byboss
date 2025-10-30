from app.db import get_db_connection


# 获取角色列表
def get_roles():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT * FROM t_role
            '''
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        print(f"Error get_roles: {e}")
    finally:
        conn.close()

#查询角色id
def get_role_by_id(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM t_role WHERE role_id = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            if result:
                # 获取角色的权限列表
                sql = "SELECT permission_id FROM t_role_permissions WHERE role_id = %s"
                cursor.execute(sql, (id,))
                permissions = cursor.fetchall()
                result['permissions'] = [p['permission_id'] for p in permissions]
            return result
    finally:
        conn.close()

#构建权限树
def get_permissions_tree():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM t_permissions ORDER BY parent_id, permission_id"
            cursor.execute(sql)
            permissions = cursor.fetchall()
            permission_tree = {}
            for permission in permissions:
                if permission['parent_id'] not in permission_tree:
                    permission_tree[permission['parent_id']] = []
                permission_tree[permission['parent_id']].append(permission)

            def build_tree(parent_id=0):
                tree = []
                if parent_id in permission_tree:
                    for permission in permission_tree[parent_id]:
                        node = {
                            'id': str(permission['permission_id']),  # 确保 id 是字符串
                            'text': permission['permission_desc'],
                            'children': build_tree(permission['permission_id'])
                        }
                        tree.append(node)
                return tree

            return build_tree()
    finally:
        conn.close()


def get_selected_permissions(role_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT permission_id FROM t_role_permissions WHERE role_id = %s", (role_id,))
            selected_permissions = [str(row['permission_id']) for row in cursor.fetchall()]
            return selected_permissions
    finally:
        conn.close()


def insert_role(role_name, permissions):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 更新角色名称
            sql = "INSERT INTO t_role (role_name) VALUES (%s)"
            cursor.execute(sql, (role_name))
            conn.commit()
            # 获取插入记录的ID
            add_role_id=cursor.lastrowid

            # 插入新的权限关联
            for permission_id in permissions:
                sql = "INSERT INTO t_role_permissions (role_id, permission_id) VALUES (%s, %s)"
                cursor.execute(sql, (add_role_id, permission_id))

            conn.commit()
    finally:
        conn.close()

def update_role(id, role_name, permissions):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 更新角色名称
            sql = "UPDATE t_role SET role_name = %s WHERE role_id = %s"
            cursor.execute(sql, (role_name, id))

            # 删除旧的权限关联
            sql = "DELETE FROM t_role_permissions WHERE role_id = %s"
            cursor.execute(sql, (id,))

            # 插入新的权限关联
            for permission_id in permissions:
                sql = "INSERT INTO t_role_permissions (role_id, permission_id) VALUES (%s, %s)"
                cursor.execute(sql, (id, permission_id))

            conn.commit()
    finally:
        conn.close()

#删除校色
def del_role_record(role_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "delete from t_role WHERE role_id = %s"
            cursor.execute(sql, (role_id,))

            # 删除旧的权限关联
            sql = "DELETE FROM t_role_permissions WHERE role_id = %s"
            cursor.execute(sql, (role_id,))
            conn.commit()
            return "success"
    except Exception as e:
        print(f"Error in company_receipts_filter: {e}")
    finally:
        conn.close()

# 添加账号
def add_user_role(user_id, role_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                INSERT INTO t_user_roles (user_id, role_id)
                VALUES (%s, %s)
            '''
            cursor.execute(sql, (user_id, role_id))
            conn.commit()
            # 获取插入记录的ID
            return cursor.lastrowid
    except Exception as e:
        print(f"Error add_user_role: {e}")
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

#获取用户权限
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