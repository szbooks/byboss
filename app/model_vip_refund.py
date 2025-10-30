import datetime

from app.db import get_db_connection
from datetime import datetime
import base64
import os
from PIL import Image
import io

# current_time = datetime.now()
# 格式化为所需的字符串表示形式（年-月-日 时:分）
# formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
# formatted_data = current_time.strftime("%Y-%m-%d")


# 读取数据转移申请列表
def get_vip_refund():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT apply.*,t_account.username as todo_user_name FROM 
                (
                SELECT t_special_apply.*,t_account.username as create_user_name FROM t_special_apply 
                LEFT JOIN t_account ON t_account.id = t_special_apply.create_account_id
                ) AS apply 
                LEFT JOIN t_account ON t_account.id = apply.todo_account_id where apply.type="r"
                ORDER BY apply.create_datetime desc
            '''
            cursor.execute(sql)
            refund = cursor.fetchall()
            # image_data_url = 'data:image/png;base64,' + b64encode(refund[0]['image_data']).decode('utf-8')
            # refund[0]['image_data']=image_data_url
            # print(refund)
            return refund
    except Exception as e:
        print(f"Error get_vip_refund: {e}")
    finally:
        conn.close()

def get_vip_refund_search(status=None,company_id=None,payment_type=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql_conditions = ["1=1"]

            if company_id not in (None, ''):
                sql_conditions.append("apply.company_id = %s")

            if status not in (None, ''):
                sql_conditions.append("apply.status = %s")

            if payment_type not in (None, ''):
                sql_conditions.append("apply.payment_type = %s")


            sql = '''
                           SELECT apply.*,t_account.username as todo_user_name FROM 
                            (
                            SELECT t_special_apply.*,t_account.username as create_user_name FROM t_special_apply 
                            LEFT JOIN t_account ON t_account.id = t_special_apply.create_account_id
                            ) AS apply 
                            LEFT JOIN t_account ON t_account.id = apply.todo_account_id where apply.type="r" and
                             ''' + " AND ".join(sql_conditions) + " ORDER BY apply.create_datetime desc"


            if company_id not in (None, '') or status not in (None, '') or payment_type not in (None, ''):
                query_params = tuple(
                    param for param in [company_id, status,payment_type]
                    if param is not None and param != '')
            print(sql)
            # cursor.execute(sql,status)
            # receipts = cursor.fetchall()
            cursor.execute(sql, query_params)
            refund = cursor.fetchall()
            return refund
    except Exception as e:
        print(f"Error get_vip_refund_search: {e}")
    finally:
        conn.close()


# 读取数据转移详情
def get_vip_refund_id(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT * FROM t_special_apply
                WHERE id = %s and type = "r"
            '''
            cursor.execute(sql, id)
            refund = cursor.fetchone()
            # image_data_url = 'data:image/png;base64,' + b64encode(refund['image_data']).decode('utf-8')
            # refund['image_data'] = image_data_url
            # print(refund)
            return refund
    except Exception as e:
        print(f"Error get_vip_refund_id: {e}")
    finally:
        conn.close()


# 更新数据转移

def update_vip_refund_status(id, status, todo_account_id=None, final_plan=None, todo_remark=None, company_id=None, phone=None, price=None, image_data=None,payment_type=None):
    """
    更新VIP退费申请状态
    参数:
        id: 申请记录ID
        status: 目标状态码
        其他参数根据状态不同可选
    """
    conn = get_db_connection()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 根据状态定义不同的SQL和参数
    sql_actions = {2: {  # 已完成
        'sql': '''
                UPDATE t_special_apply
                SET status=%s, todo_remark=%s, todo_account_id=%s, 
                    todo_datetime=%s, final_plan=%s, company_id=%s, 
                    phone=%s, price=%s, image_data=%s,payment_type=%s
                WHERE id=%s
            ''', 'params': (status, todo_remark, todo_account_id, current_time, final_plan, company_id, phone, price, image_data,payment_type, id)}, 3: {  # 已拒绝
        'sql': '''
                UPDATE t_special_apply
                SET status=%s, todo_remark=%s, todo_account_id=%s, 
                    todo_datetime=%s, final_plan=%s, company_id=%s, 
                    phone=%s, price=%s, image_data=%s,payment_type=%s
                WHERE id=%s
            ''', 'params': (status, todo_remark, todo_account_id, current_time, final_plan, company_id, phone, price, image_data, payment_type,id)}, 8: {  # 保存草稿
        'sql': '''
                UPDATE t_special_apply
                SET todo_remark=%s, final_plan=%s, company_id=%s, 
                    phone=%s, price=%s, image_data=%s,payment_type=%s
                WHERE id=%s
            ''', 'params': (todo_remark, final_plan, company_id, phone, price, image_data, payment_type,id)}, 4: {  # 保存备注
        'sql': '''
                UPDATE t_special_apply
                SET todo_remark=%s, price=%s
                WHERE id=%s
            ''', 'params': (todo_remark, price, id)}}

    try:
        with conn.cursor() as cursor:
            action = sql_actions.get(status)
            if not action:
                raise ValueError(f"无效的状态码: {status}")

            cursor.execute(action['sql'], action['params'])
            conn.commit()

    except Exception as e:
        print(f"更新VIP退费状态失败: {str(e)}")
        raise  # 重新抛出异常供上层处理
    finally:
        conn.close()


# 申请vip退费
def add_new_vip_refund(company_id, phone, content, create_account_id, todo_account_id, type,price,card_back_image=None,payment_type=None):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    conn = get_db_connection()

    try:

        # processed_images = {'card_back': process_image_data(card_back_image)}


        with conn.cursor() as cursor:
            sql = '''
                            INSERT INTO `dh_support`.`t_special_apply` (`company_id`, `phone`, `content`, `status`, `create_account_id`, `create_datetime`, `todo_account_id`,type,price,image_data,payment_type) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s);
                        '''
            if create_account_id==3:
                status = 2
            else:
                status = 1
            # current_time = datetime.datetime.now()
            cursor.execute(sql, (company_id, phone,content,status, create_account_id, formatted_time, todo_account_id,type,price,card_back_image,payment_type))
            # cursor.execute(sql, (company_id, phone, content, status, create_account_id, formatted_time, todo_account_id, type, image_data))
            conn.commit()
            # 获取插入记录的ID
            return cursor.lastrowid
    except Exception as e:
        print(f"Error add_new_vip_refund: {e}")
    finally:
        conn.close()

def process_image_data(image_data, max_size=(1024, 1024), quality=85):
    """
    处理图片数据（支持 base64 字符串或文件对象），并返回纯 base64 数据（不带前缀）

    参数:
        image_data: base64 字符串或文件对象
        max_size: 最大尺寸 (宽, 高)
        quality: 压缩质量 (0-100)

    返回:
        处理后的纯 base64 字符串（不带 `data:image/...` 前缀），或 None（如果输入无效）
    """
    if not image_data:
        return None

    try:
        # 如果是 base64 字符串（以 'data:image' 开头）

        image_bytes = base64.b64decode(image_data)
        # 如果是文件对象（如 Flask 的 request.files）

        # 打开图片并处理
        img = Image.open(io.BytesIO(image_bytes))

        # 转换为 RGB（如果是 RGBA 或 P 模式）
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # 调整大小（保持宽高比）
        img.thumbnail(max_size, Image.LANCZOS)

        # 压缩并转换为 base64
        output_buffer = io.BytesIO()
        img.save(output_buffer, format='JPEG', quality=quality)
        processed_bytes = output_buffer.getvalue()

        # 返回纯 base64 字符串（不带前缀）
        return base64.b64encode(processed_bytes).decode('utf-8')

    except Exception as e:
        print(f"图片处理失败: {str(e)}")
        return None

#删除vip
def del_vip_record(vip_refund_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                 DELETE from t_special_apply where id=%s and type="r"
             '''
            cursor.execute(sql, (vip_refund_id,))
            conn.commit()
            return "success"
    except Exception as e:
        print(f"Error in company_receipts_filter: {e}")
    finally:
        conn.close()


#编辑vo[
def edit_vip_data(id, phone, content, company_id,price,payment_type,image_path):
    conn = get_db_connection()
    current_time = datetime.now()
    sql = ""

    try:
        with conn.cursor() as cursor:
            sql = '''
                UPDATE t_special_apply
                SET phone=%s, company_id=%s, content=%s,price=%s, image_data=%s,payment_type=%s
                WHERE id = %s and type="r"
            '''
            cursor.execute(sql, (phone, company_id, content,price,image_path,payment_type,id))
            conn.commit()


    except Exception as e:
        print(f"Error in edit_discount_data: {e}")

    finally:
        conn.close()
