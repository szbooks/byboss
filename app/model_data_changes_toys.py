import datetime

from app.db import get_db_connection, get_db_connection_w
from datetime import datetime


def get_data_changes_result(company_id,room_num):
    conn = get_db_connection_w()
    try:
        with conn.cursor() as cursor:



            # 构建最终的 SQL 查询
                sql = '''
                    SELECT * FROM t_guide_video 
                    WHERE ''' + " AND ".join(sql_conditions) + " ORDER BY create_time DESC"

                # 执行查询
                cursor.execute(sql, query_params)
                results = cursor.fetchall()
            else:
                sql = '''
                                    SELECT * FROM t_guide_video  ORDER BY create_time DESC'''

                # 执行查询
                cursor.execute(sql)
                results = cursor.fetchall()


            return results
    except Exception as e:
        print(f"Error in get_vguide_video: {e}")
        return []  # 返回空列表，避免返回 None
    finally:
        conn.close()

def add_new_guide_video(video_name, video_address, remark,type="2"):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            sql = '''       
                     INSERT INTO `dh_support`.`t_guide_video` (`video_name`, `video_address`, `remark`, `create_time`,type) VALUES (%s, %s, %s, %s,%s);
                            
                        '''

            # current_time = datetime.datetime.now()
            cursor.execute(sql, (video_name, video_address, remark,formatted_time,type))
            conn.commit()
            # 获取插入记录的ID
            return cursor.lastrowid
    except Exception as e:
        print(f"Error add_new_guide_video: {e}")
    finally:
        conn.close()

#获取编辑数据
def get_guide_video(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                select * from  t_guide_video where id=%s
            '''
            cursor.execute(sql, id)
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(f"Error get_api: {e}")
    finally:
        conn.close()

#更新推送地址
def updata_guide_video(id,video_name,video_address,remark,type):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                UPDATE t_guide_video SET video_name=%s,video_address=%s,remark=%s,type=%s WHERE (`id`=%s);
            '''
            cursor.execute(sql,(video_name,video_address,remark,type,id))
            conn.commit()

    except Exception as e:
        print(f"Error get_api: {e}")
    finally:
        conn.close()