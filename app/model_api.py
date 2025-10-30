import datetime
from contextlib import closing

from app.db import get_db_connection, get_db_connection_read, get_db_connection_w
from datetime import datetime

from app.utils import md5_encrypt


# current_time = datetime.now()
# 格式化为所需的字符串表示形式（年-月-日 时:分）
# formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
# formatted_data = current_time.strftime("%Y-%m-%d")


# 读取数据转移申请列表
def get_api_list(company_id=None,channel_address=None,appid=None,yuming=None):
    conn = get_db_connection()
    connread = get_db_connection_read()

    try:
        with connread.cursor() as cursor:
            sql_conditions = ["1=1"]

            if company_id not in (None, ''):
                sql_conditions.append("opc.granted_company_id = %s")

            if channel_address not in (None, '',"None"):
                sql_conditions.append("op.config like %s")
                channel_address="%"+channel_address+"%"
            if appid not in (None, ''):
                sql_conditions.append("op.app_id = %s")

            if yuming not in (None, ''):
                sql_conditions.append("op.config like %s")
                yuming = "%" + yuming + "%"


            sql = '''
                      select opc.granted_company_id,op.id,op.name,op.app_id,op.app_secret,op.state,op.config,left(op.create_time,10)create_time from
                open_partner_company opc join open_partner op on opc.app_id=op.app_id where '''+" AND ".join(sql_conditions) + " ORDER BY op.app_id desc"

            sql_count = '''
                                  select count(*)total_count from
                            open_partner_company opc join open_partner op on opc.app_id=op.app_id where ''' + " AND ".join(sql_conditions) + " ORDER BY op.app_id desc"

            if company_id not in (None, '') or channel_address not in (None, '', 'None') or appid not in (None, '') or yuming not in (None, ''):
                query_params = tuple(param for param in [company_id, channel_address, appid, yuming] if param not in (None, '', 'None')  # 排除 None、空字符串和字符串 'None'
                )
                print(sql)
                cursor.execute(sql, query_params)
                results = cursor.fetchall()
                cursor.execute(sql_count, query_params)
                total_count = cursor.fetchone()['total_count']
            else:
                cursor.execute(sql)
                results = cursor.fetchall()
                cursor.execute(sql_count)
                total_count = cursor.fetchone()['total_count']




            # print(sql)
            # cursor.execute(sql)
            # results = cursor.fetchall()
            return results,total_count
    except Exception as e:
        print(f"Error get_coop_ex: {e}")
    finally:
        conn.close()
        connread.close()





# 读取数据
def get_channel():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT * FROM t_api_channel
            '''
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Error get_coop_id: {e}")
    finally:
        conn.close()

#获取编辑数据
def get_api(id):
    conn_read = get_db_connection_read()
    try:
        with conn_read.cursor() as cursor:
            sql = '''
                select opc.granted_company_id,op.id,op.name,op.app_id,op.app_secret,op.state,op.config,left(op.create_time,10)create_time from
                open_partner_company opc join open_partner op on opc.app_id=op.app_id where op.id=%s
            '''
            cursor.execute(sql, id)
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(f"Error get_api: {e}")
    finally:
        conn_read.close()

#更新推送地址
def updata_pushadd(id,push_add):
    conn_w = get_db_connection_w()
    try:
        with conn_w.cursor() as cursor:
            sql = '''
                UPDATE open_partner SET config=%s WHERE (`id`=%s);
            '''
            cursor.execute(sql,(push_add,id))
            conn_w.commit()

    except Exception as e:
        print(f"Error get_api: {e}")
    finally:
        conn_w.close()

# 更新数据

def update_api_data(company_id=None, channel_id=None, channel_name="", pushaddress=""):
    conn = get_db_connection()
    conn_w = get_db_connection_w()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    appid=""
    secret=""
    if pushaddress in (None,""):
        pushaddress="{}"
    try:
        # 使用 with 语句确保游标在使用完毕后被关闭
        with closing(conn_w.cursor()) as cursor:
            if company_id not in (None, ""):
                phone = "11111111111" + company_id
                sql = '''
                        select * from open_partner_company where granted_company_id=%s
                    '''

                cursor.execute(sql, (company_id))
                company_result = cursor.fetchone()
                if company_result:
                    result = 1
                    return result,appid,secret,pushaddress,company_id

                get_phone_sql = '''
                          select company_name,if(offical_remark is NULL,%s,offical_remark)phone from company where id=%s
                                   '''
                cursor.execute(get_phone_sql, (phone, company_id))
                data_result = cursor.fetchone()
                if not data_result:
                    result = 2
                    return result, appid, secret, pushaddress, company_id

                company_name = data_result["company_name"]
                company_phone = data_result["phone"]

                phone_confirm_sql = '''
                                                        select count(*) from open_partner where mobile=%s
                                                                  '''
                cursor.execute(phone_confirm_sql, (company_phone))
                phone_confirm_result = cursor.fetchone()

                if phone_confirm_result:
                    company_phone=phone

                get_appid_sql = '''
                    select max(id)+1 appid from open_partner
                '''
                cursor.execute(get_appid_sql)
                appid_result = cursor.fetchone()
                appid = appid_result["appid"]
                secret = md5_encrypt(str(appid))

                print("secret", secret)
                appid_insert_sql = '''
                    INSERT INTO `dh_short_rent`.`open_partner` (`id`, `name`, `mobile`, `password`, `app_id`, `app_secret`, `state`, `config`, `create_time`) 
                    VALUES (%s,%s,%s,'',%s,%s,'S',%s,%s);    
                '''
                cursor.execute(appid_insert_sql, (appid, company_name, company_phone, appid, secret, pushaddress, formatted_time))
                conn_w.commit()


                appid2_insert_sql = '''
                                            INSERT INTO `dh_short_rent`.`open_partner_company` (`app_id`, `granted_company_id`, `scope`, `create_time`) VALUES (%s, %s, 'account',%s);   
                                        '''
                cursor.execute(appid2_insert_sql, (appid, company_id, formatted_time))
                conn_w.commit()
                print("接口创建成功")
                result = 0

        with closing(conn.cursor()) as cursor:
            if channel_id not in (None, '',"new") and channel_name not in (None, '') and  pushaddress not in (None, ''):
                t_api_channel_insert_sql = '''
                             UPDATE `dh_support`.`t_api_channel` SET `address`=%s WHERE (`id`=%s);
                                                                                 '''
                cursor.execute(t_api_channel_insert_sql, (pushaddress,channel_id))
                conn.commit()

            if channel_id=="new" and channel_name not in (None, '') and  pushaddress not in (None, ''):
                t_api_channel_insert2_sql = '''
                       INSERT INTO `dh_support`.`t_api_channel` (`channel`, `address`) VALUES (%s,%s);
                                                                                                     '''
                cursor.execute(t_api_channel_insert2_sql, (channel_name, pushaddress))
                conn.commit()

        return result,appid,secret,pushaddress,company_id


    except Exception as e:
        conn.rollback()
        print(f"Error update_coop_ex: {e}")

    finally:
    # 关闭数据库连接
        conn.close()

