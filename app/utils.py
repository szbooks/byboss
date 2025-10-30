from collections import defaultdict

from app.db import get_db_connection, get_db_connection_read
import hashlib
import re
import string
import os
import requests
import threading
from datetime import datetime

#后端分页
def paginate(query, page, per_page):

    if query is None:
        return [], 0, 1

    # 计算分页的起始位置
    start = (page - 1) * per_page
    end = start + per_page

    # 获取当前页的数据
    paginated_data = query[start:end]

    # 计算总记录数
    total_records = len(query)

    # 计算总页数
    total_pages = total_records // per_page + (1 if total_records % per_page > 0 else 0)

    return paginated_data, total_records, total_pages

#账号姓名查询
def get_username(userid):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                select username from t_account where id=%s
            '''
            cursor.execute(sql,userid)
            results = cursor.fetchone()
            return results
    except Exception as e:
        print(f"Error get_discounts: {e}")
    finally:
        conn.close()


#账号姓名查询
def get_username_byrole(role_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT t_account.id,t_account.username,t_account.realname,role_id FROM `t_account` join t_user_roles on t_account.id=t_user_roles.user_id where t_user_roles.role_id in (%s) or t_account.id=3 or t_account.id=9 or t_account.id=19;
            '''
            cursor.execute(sql,role_id)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Error get_discounts: {e}")
    finally:
        conn.close()

#md5加密
    # """
    # 使用MD5算法对文本进行加密
    #
    # :param text: 需要加密的文本字符串
    # :return: 加密后的MD5哈希值（十六进制表示）
    # """
def md5_encrypt(text):

    # 创建一个md5对象
    md5_hash = hashlib.md5()

    # 更新md5对象的内容，注意需要将字符串转换为字节串
    md5_hash.update(text.encode('utf-8'))

    # 获取十六进制表示的哈希值
    encrypted_text = md5_hash.hexdigest()

    return encrypted_text


def is_integer(s):
    # 定义正则表达式模式，匹配整数
    pattern = r'^-?\d+$'

    # 使用 re.match 函数进行匹配
    return bool(re.match(pattern, s))

#去除标点符号、转换为小写、分词
def preprocess_text(text):
    # 去除标点符号
    text = text.translate(str.maketrans('', '', string.punctuation))
    # 转换为小写
    text = text.lower()
    # 分词
    words = text.split()
    return words

#多线程下载
# image_urls = [
#     "https://example.com/image1.jpg",
#     "https://example.com/image2.jpg",
#     "https://example.com/image3.jpg"
# ]

def download(save_dir,image_urls):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    def download_image(url):
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(save_dir, url.split("/")[-1])
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Downloaded {url} to {filename}")
        else:
            print(f"Failed to download {url}")

    # 创建线程
    threads = []
    for url in image_urls:
        thread = threading.Thread(target=download_image, args=(url,))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

#更新客户运营人员公司数据-批量
def updata_operating_sub():
    conn = get_db_connection()
    connread = get_db_connection_read()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    # data_dict = {}
    data_dict = defaultdict(list)

    try:
        with conn.cursor() as cursor:
            get_phone_sql = '''
                select id,phone from t_operating_sub;
            '''
            cursor.execute(get_phone_sql)
            results = cursor.fetchall()
        with connread.cursor() as cursor:
            if results:
                for result in results:
                    company_ids = []
                    get_companys_sql = '''
                                   select company_id from user where mobile=%s and empl_type="E"; 
                               '''
                    cursor.execute(get_companys_sql, (result['phone']))
                    result_companys = cursor.fetchall()
                    if result_companys:
                        for result_company in result_companys:
                            company_id = result_company['company_id']  # 根据实际字段索引调整
                            # company_ids.append(str(company_id))
                            data_dict[result['id']].append(company_id)
                        # company_ids_str = ','.join(company_ids)

                    else:
                        company_id = ""
                        data_dict[result['id']].append(company_id)
                # data_dict[result['id']] = company_ids_str
                # data_dict = {key: ','.join(values) for key, values in data_dict.items()}
        with conn.cursor() as cursor:
            for key, values in data_dict.items():
                # 将列表转换为以逗号分隔的字符串
                values_str = ','.join(map(str, values))
                updata_sql = '''
                    UPDATE `dh_support`.`t_operating_sub` SET `company_id`=%s,`update_date`=%s WHERE (`id`=%s);
                '''

                cursor.execute(updata_sql, ({values_str},formatted_time,{key}))
                conn.commit()



    except Exception as e:
        print(f"Error updata_operating_sub: {e}")
    finally:
        conn.close()

#更新客户运营人员公司数据-单个手机号码
def updata_operating_sub_singer(phone):
    conn = get_db_connection()
    connread = get_db_connection_read()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    # data_dict = {}
    data_dict = defaultdict(list)

    try:
        with conn.cursor() as cursor:
            get_phone_sql = '''
                select id,phone from t_operating_sub where phone=%s;
            '''
            cursor.execute(get_phone_sql, phone)
            result = cursor.fetchone()
        with connread.cursor() as cursor:
            get_companys_sql = '''
                           select company_id from user where mobile=%s and empl_type="E"; 
                       '''
            cursor.execute(get_companys_sql, (result['phone']))
            result_companys = cursor.fetchall()

            if result_companys:
                for result_company in result_companys:
                    company_id = result_company['company_id']  # 根据实际字段索引调整
                    # company_ids.append(str(company_id))
                    data_dict[result['id']].append(company_id)
                # company_ids_str = ','.join(company_ids)

            else:
                company_id = ""
                data_dict[result['id']].append(company_id)
        # data_dict[result['id']] = company_ids_str
        # data_dict = {key: ','.join(values) for key, values in data_dict.items()}
        with conn.cursor() as cursor:
            for key, values in data_dict.items():
                # 将列表转换为以逗号分隔的字符串
                values_str = ','.join(map(str, values))
                updata_sql = '''
                    UPDATE `dh_support`.`t_operating_sub` SET `company_id`=%s,`update_date`=%s WHERE (`id`=%s);
                '''

                cursor.execute(updata_sql, ({values_str},formatted_time,{key}))
                conn.commit()
    except Exception as e:
        print(f"Error get_discounts: {e}")
    finally:
        conn.close()





