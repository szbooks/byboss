# models/analysis_model.py
import sys

from . import db  # 假设已有db实例
from app.db import get_db_connection


class AnalysisData:
    @staticmethod
    def get_analysis_data():

        # 创建数据库连接
        conn = get_db_connection()

        try:
            with (conn.cursor() as cursor):

                sql = '''
                            select * from (select a.taskid,a.company_id,if(c.room_count is null,0,c.room_count)room_count,
CAST(COALESCE(JSON_UNQUOTE(JSON_EXTRACT(regi_infor, '$.roomCount')), '0') AS UNSIGNED) AS regi_roomCount,c.regi_infor,
JSON_UNQUOTE(JSON_EXTRACT(regi_infor, '$.companyType')) AS companyType
from t_presales_progress a LEFT JOIN t_company c on a.company_id=c.company_id where a.progress_state not in ("4","6") and left(c.create_time,10)>="2025-07-31")a'''

                cursor.execute(sql)

                # 获取查询结果
                data_results = cursor.fetchall()
                return data_results

        except Exception as e:
            print(f"Error get_analysis_data: {e}")

        finally:
            conn.close()

    @staticmethod
    def save_data(results):
        """
        将分析结果批量保存到数据库（全量更新模式）
        参数:
            results: 字典列表，每个字典包含company_id和star字段
                   示例: [{"company_id": 1, "star": 5}, ...]
        返回:
            int: 执行更新的记录数（全量更新，无论值是否变化）
        """
        if not results:
            print("警告: 空结果集，无需更新")
            return 0

        conn = None
        updated_rows = 0

        try:
            # 创建数据库连接
            conn = get_db_connection()

            with conn.cursor() as cursor:
                # 准备批量更新SQL（全量更新）
                update_sql = '''
                    UPDATE t_presales_progress 
                    SET stars = %s 
                    WHERE company_id = %s
                '''

                # 构造参数列表 [(star, company_id), ...]
                params = [(result['star'], result['company_id']) for result in results if 'company_id' in result and 'star' in result]

                if not params:
                    print("错误: 结果数据缺少必要字段")
                    return 0

                # 执行批量更新（全量）
                cursor.executemany(update_sql, params)
                updated_rows = len(params)  # 改为返回参数列表长度（全量计数）

                # 提交事务
                conn.commit()

            return updated_rows

        except Exception as e:
            # 错误处理
            if conn:
                conn.rollback()
            print(f"数据库更新失败: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return 0

        finally:
            # 确保连接关闭
            if conn:
                conn.close()

