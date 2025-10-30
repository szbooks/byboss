import datetime

from app.db import get_db_connection
from datetime import datetime
from base64 import b64encode

from datetime import datetime
from flask import jsonify
import base64
import os
from PIL import Image
import io


# current_time = datetime.now()
# 格式化为所需的字符串表示形式（年-月-日 时:分）
# formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
# formatted_data = current_time.strftime("%Y-%m-%d")


# 读取数据转移申请列表
def get_shop_owner_change():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT shop.*,t_account.username as todo_user_name FROM 
                (
                SELECT t_shop_owner_change.*,t_account.username as create_user_name FROM t_shop_owner_change 
                LEFT JOIN t_account ON t_account.id = t_shop_owner_change.create_account_id
                ) AS shop 
                LEFT JOIN t_account ON t_account.id = shop.todo_account_id 
                ORDER BY shop.create_datetime desc
            '''
            cursor.execute(sql)
            results = cursor.fetchall()

            return results
    except Exception as e:
        print(f"Error get_shop_owner_change: {e}")
    finally:
        conn.close()


def get_shop_owner_change_search(status=None, company_id=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql_conditions = ["1=1"]

            if company_id not in (None, ''):
                sql_conditions.append("shop.company_id = %s")

            if status not in (None, ''):
                sql_conditions.append("shop.status = %s")

            sql = '''
                           SELECT shop.*,t_account.username as todo_user_name FROM 
                (
                SELECT t_shop_owner_change.*,t_account.username as create_user_name FROM t_shop_owner_change 
                LEFT JOIN t_account ON t_account.id = t_shop_owner_change.create_account_id
                ) AS shop 
                LEFT JOIN t_account ON t_account.id = shop.todo_account_id where 
                             ''' + " AND ".join(sql_conditions) + " ORDER BY shop.create_datetime desc"

            if company_id not in (None, '') or status not in (None, ''):
                query_params = tuple(param for param in [company_id, status] if param is not None and param != '')
            print(sql)
            # cursor.execute(sql,status)
            # receipts = cursor.fetchall()
            cursor.execute(sql, query_params)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Error get_shop_owner_change_search: {e}")
    finally:
        conn.close()


# 读取数据转移详情
def get_shop_owner_change_id(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                select id,company_id,content,old_owner,new_owner,todo_remark,
IFNULL(license_image_data, '') AS license_image_data,
IFNULL(card_front_image, '') AS card_front_image,
IFNULL(card_back_image, '') AS card_back_image
from t_shop_owner_change where id=%s
            '''
            cursor.execute(sql, id)
            resultid = cursor.fetchone()

            return resultid
    except Exception as e:
        print(f"Error get_shop_owner_change_id: {e}")
    finally:
        conn.close()


# 申请更换店主
def add_new_shop_owner_change(company_id, new_owner, content, current_user_id, todo_userid, card_front_image=None, card_back_image=None, license_image_data=None, status="pending"):
    """
    新增店主更换申请 (优化版)

    参数:
        company_id: 公司ID (必填)
        new_owner: 新店主
        content: 申请内容 (必填)
        current_user_id: 当前用户ID (必填)
        todo_userid: 待办用户ID (必填)
        card_front_image: 身份证正面(base64或文件对象)
        card_back_image: 身份证反面(base64或文件对象)
        license_image_data: 营业执照(base64或文件对象)
        status: 状态 (默认'pending')
    """
    # 验证必填参数
    if not all([company_id, current_user_id, todo_userid]):
        raise ValueError("缺少必填参数")

    # 准备数据
    create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = None

    try:
        # 处理图片数据
        processed_images = {'card_front': process_image_data(card_front_image), 'card_back': process_image_data(card_back_image), 'license': process_image_data(license_image_data)}

        # 获取数据库连接
        conn = get_db_connection()

        with conn.cursor() as cursor:
            sql = '''
                INSERT INTO `dh_support`.`t_shop_owner_change` 
                (`company_id`, `content`, `new_owner`, 
                 `license_image_data`, `card_front_image`, `card_back_image`, 
                 `status`, `create_account_id`, `create_datetime`, `todo_account_id`) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            '''
            params = (company_id, content, new_owner, processed_images['license'], processed_images['card_front'], processed_images['card_back'], status, current_user_id, create_time, todo_userid)

            cursor.execute(sql, params)
            conn.commit()

            # 返回新记录的ID
            return cursor.lastrowid

    except Exception as e:
        print(f"新增店主更换申请失败: {str(e)}", exc_info=True)
        # 回滚事务
        if conn:
            conn.rollback()
        raise  # 重新抛出异常供上层处理

    finally:
        if conn:
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


# 删除vip
def del_shop_owner_change_record(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                 DELETE from t_shop_owner_change where id=%s;
             '''
            cursor.execute(sql, (id,))
            conn.commit()
            return "success"
    except Exception as e:
        print(f"Error in company_receipts_filter: {e}")
    finally:
        conn.close()


# 编辑
def edit_shop_owner_change_data(id, company_id, new_owner, content, card_front_image, card_back_image, license_image_data):
    conn = None
    try:
        conn = get_db_connection()
        current_time = datetime.now()

        sql = """
            UPDATE `dh_support`.`t_shop_owner_change`
            SET `company_id`=%s, `new_owner`=%s, `content`=%s, 
                `card_front_image`=%s, `card_back_image`=%s, `license_image_data`=%s
            WHERE `id`=%s;
        """

        # 执行更新
        with conn.cursor() as cursor:
            # 将所有参数打包成一个元组
            cursor.execute(sql, (company_id, new_owner, content, card_front_image, card_back_image, license_image_data, id))
            conn.commit()

        return True

    except Exception as e:
        print(f"更新店主更换申请失败: {str(e)}")
        if conn:
            conn.rollback()
        return False

    finally:
        if conn:
            conn.close()


# 处理
def do_shop_owner_change_data(id, company_id, new_owner, final_plan, todo_remark, status, card_front_image, card_back_image, license_image_data, action):
    conn = None
    try:
        conn = get_db_connection()
        current_time = datetime.now()

        if action == "completed":

            sql = """
                UPDATE `dh_support`.`t_shop_owner_change`
                SET `company_id`=%s, `new_owner`=%s, `final_plan`=%s, `todo_remark`=%s,todo_datetime=%s, status=%s,
                    `card_front_image`=%s, `card_back_image`=%s, `license_image_data`=%s
                WHERE `id`=%s;"""

            with conn.cursor() as cursor:
                cursor.execute(sql, (company_id, new_owner, final_plan, todo_remark, current_time, status, card_front_image, card_back_image, license_image_data, id))
                conn.commit()
        elif action == "save":
            sql = """
                            UPDATE `dh_support`.`t_shop_owner_change`
                            SET `company_id`=%s, `new_owner`=%s, `final_plan`=%s, `todo_remark`=%s WHERE `id`=%s;"""

            with conn.cursor() as cursor:
                cursor.execute(sql, (company_id, new_owner, final_plan, todo_remark, id))
                conn.commit()

        # 执行更新

        return True

    except Exception as e:
        print(f"处理店主更换失败: {str(e)}")
        if conn:
            conn.rollback()
        return False

    finally:
        if conn:
            conn.close()


def update_remark(id, remark):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                     UPDATE `dh_support`.`t_shop_owner_change` SET todo_remark=%s WHERE id=%s;
                 '''
            cursor.execute(sql, (remark, id))
            conn.commit()
            return "success"
    except Exception as e:
        print(f"Error in company_receipts_filter: {e}")
    finally:
        conn.close()
