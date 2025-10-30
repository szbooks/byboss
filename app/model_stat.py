from app.db import get_db_connection


# 获取统计数据-公司
def get_stat_company(page, per_page):
    # 计算起始记录
    start = (page - 1) * per_page

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 编写SQL查询，使用LIMIT进行分页
            sql = '''
                SELECT tsp.*, 
                tsp1.countday countday_y,tsp1.company_new company_new_y,tsp1.company_new_invited,tsp1.company_activate company_activate_y,tsp1.company_protect company_protect_y,tsp1.company_freeze company_freeze_y,
                tsp1.company_postpone company_postpone_y,tsp1.pay_company pay_company_y,tsp1.pay_num pay_num_y,tsp1.pay_value pay_value_y,tsp1.pay_company_invited pay_company_invited_y,
                tsp1.pay_company_invited_value pay_company_invited_value_y,tsp1.pay_annual_company pay_annual_company_y,tsp1.pay_annual_value pay_annual_value_y,tsp1.pay_first_company pay_first_company_y,
                tsp1.pay_first_value pay_first_value_y,tsp1.pay_first_annual_company pay_first_annual_company_y,tsp1.pay_first_annual_value pay_first_annual_value_y,tsp1.create_time create_time_y
                FROM t_stat_pay tsp 
                left join t_stat_pay tsp1 on DATE_SUB(tsp.countday, INTERVAL 1 YEAR)=tsp1.countday order by tsp.countday desc 
                LIMIT %s OFFSET %s
            '''
            cursor.execute(sql, (per_page, start))
            items = cursor.fetchall()

            # 获取总记录数
            sql = '''
                SELECT COUNT(*), 
                tsp1.countday countday_y,tsp1.company_new company_new_y,tsp1.company_new_invited,tsp1.company_activate company_activate_y,tsp1.company_protect company_protect_y,tsp1.company_freeze company_freeze_y,
                tsp1.company_postpone company_postpone_y,tsp1.pay_company pay_company_y,tsp1.pay_num pay_num_y,tsp1.pay_value pay_value_y,tsp1.pay_company_invited pay_company_invited_y,
                tsp1.pay_company_invited_value pay_company_invited_value_y,tsp1.pay_annual_company pay_annual_company_y,tsp1.pay_annual_value pay_annual_value_y,tsp1.pay_first_company pay_first_company_y,
                tsp1.pay_first_value pay_first_value_y,tsp1.pay_first_annual_company pay_first_annual_company_y,tsp1.pay_first_annual_value pay_first_annual_value_y,tsp1.create_time create_time_y
                FROM t_stat_pay tsp left join t_stat_pay tsp1 on DATE_SUB(tsp.countday, INTERVAL 1 YEAR)=tsp1.countday order by tsp.countday desc 
             '''
            cursor.execute(sql)
            total_count = cursor.fetchone()['COUNT(*)']

            return items, total_count
    except Exception as e:
        print(f"Error get_stat_company: {e}")
    finally:
        conn.close()


# 获取统计数据-付费
def get_stat_pay():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
               SELECT tsp.*, 
tsp1.countday countday_y,tsp1.company_new company_new_y,tsp1.company_new_invited,tsp1.company_activate company_activate_y,tsp1.company_protect company_protect_y,tsp1.company_freeze company_freeze_y,
tsp1.company_postpone company_postpone_y,tsp1.pay_company pay_company_y,tsp1.pay_num pay_num_y,tsp1.pay_value pay_value_y,tsp1.pay_company_invited pay_company_invited_y,
tsp1.pay_company_invited_value pay_company_invited_value_y,tsp1.pay_annual_company pay_annual_company_y,tsp1.pay_annual_value pay_annual_value_y,tsp1.pay_first_company pay_first_company_y,
tsp1.pay_first_value pay_first_value_y,tsp1.pay_first_annual_company pay_first_annual_company_y,tsp1.pay_first_annual_value pay_first_annual_value_y,tsp1.create_time create_time_y
FROM t_stat_pay tsp left join t_stat_pay tsp1 on DATE_SUB(tsp.countday, INTERVAL 1 YEAR)=tsp1.countday order by tsp.countday desc
            '''
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Error get_stat_pay: {e}")
    finally:
        conn.close()


# 获取统计数据-首次付费
def get_stat_pay_first():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT tsp.*, 
tsp1.countday countday_y,tsp1.company_new company_new_y,tsp1.company_new_invited,tsp1.company_activate company_activate_y,tsp1.company_protect company_protect_y,tsp1.company_freeze company_freeze_y,
tsp1.company_postpone company_postpone_y,tsp1.pay_company pay_company_y,tsp1.pay_num pay_num_y,tsp1.pay_value pay_value_y,tsp1.pay_company_invited pay_company_invited_y,
tsp1.pay_company_invited_value pay_company_invited_value_y,tsp1.pay_annual_company pay_annual_company_y,tsp1.pay_annual_value pay_annual_value_y,tsp1.pay_first_company pay_first_company_y,
tsp1.pay_first_value pay_first_value_y,tsp1.pay_first_annual_company pay_first_annual_company_y,tsp1.pay_first_annual_value pay_first_annual_value_y,tsp1.create_time create_time_y
FROM t_stat_pay tsp left join t_stat_pay tsp1 on DATE_SUB(tsp.countday, INTERVAL 1 YEAR)=tsp1.countday order by tsp.countday desc
            '''
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Error get_stat_pay_first: {e}")
    finally:
        conn.close()

# 获取统计数据-核心数据
def get_stat_operate():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                select * from t_stat_operate ORDER BY stat_day desc;
            '''
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)

            sql = '''
SELECT
	tso.stat_day,
	tso.pay_company,
	tso.pay_room,
	tso.weshop_company,
	tso.xhsshop_company,
	tso.pay_bonus,
	a.*
FROM
	(
		SELECT
			LAST_DAY(stat_day) AS last_day_of_month,
			LEFT (stat_day, 7) months,
			CAST(SUM(new_company) AS SIGNED) total_nc,
			CAST(SUM(net_pay_company) AS SIGNED) total_npc,
			CAST(SUM(new_room) AS SIGNED) total_nr,
			CAST(SUM(net_pay_room) AS SIGNED) total_npr,
			SUM(pay_vip) total_pv,
			sum(pay_revenue) total_pr,
			sum(pay_revenue_roomfee) total_prr,
			sum(pay_revenue_deposit) total_prd,
			sum(pay_revenue_weroomfee) total_prw,
			CAST(SUM(per_contract) AS SIGNED)total_pc,
			CAST(SUM(pay_per_contract) AS SIGNED)total_ppc
		FROM
			t_stat_operate
		GROUP BY
			YEAR (stat_day),
			MONTH (stat_day)
	) a
JOIN t_stat_operate tso ON a.last_day_of_month = tso.stat_day ORDER BY a.months desc;
                       '''
            cursor.execute(sql)
            sumresults = cursor.fetchall()

            # sql = '''
            #                 select pay_company from t_stat_operate ORDER BY stat_day desc LIMIT 1
            #                        '''
            # cursor.execute(sql)
            # last_data = cursor.fetchall()
            # sumresults=tuple(sumresults)+tuple(last_data)
            # sumresults = sumresults + last_data
            # print(sumresults)
            return results,sumresults
    except Exception as e:
        print(f"Error get_stat_operate: {e}")
    finally:
        conn.close()


# 获取统计数据-试用期
def get_stat_period():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                                       select b.custom_type,b.统计月份 idx_data,b.总数 sumcount,(b.待续费-b.特殊处理)no_Renewal,(b.续费数+b.特殊处理)renew_stat,b.过期数 expire_stat,b.未激活数 noactive_stat,b.特殊处理 special_stat,CONCAT(CAST(round((((b.续费数+b.特殊处理)/(b.总数-b.未激活数)))*100,2) AS CHAR),'%')Renewal_ratio,
                    CONCAT(CAST(round(((b.过期数/(b.总数-b.未激活数)))*100,2) AS CHAR),'%')Loss_rate,
                    CONCAT(CAST(round(((b.未激活数/(b.总数)))*100,2) AS CHAR),'%')noactive_rate
                     from (
                    select custom_type,idx_data 统计月份,count(housing_num)总数,count(a.no_Renewal)待续费,count(isRenewal)续费数,count(isexpire)过期数,count(IF(company is not null and activation_day IS NULL, 1, NULL))未激活数,
                    count(IF(TIMESTAMPDIFF(MONTH, activation_day, end_day)>=2 and isRenewal is null and isexpire is null, 1, NULL))特殊处理
                    ,CONCAT(CAST(round((count(isRenewal)/count(*))*100,2) AS CHAR),'%')续费比
                    ,CONCAT(CAST(round((count(isexpire)/count(*))*100,2) AS CHAR),'%')流失率
                    from (
                    select if(isexpire is null and isRenewal is null and activation_day is not null,1,null)no_Renewal,t_Unpaid_count.*
                    from t_Unpaid_count)a
                    where housing_num is not null and a.custom_type="w" 
                    GROUP BY idx_data)b
                    UNION ALL
                    select b.custom_type,b.统计月份 idx_data,b.总数 sumcount,(b.待续费-b.特殊处理)no_Renewal,(b.续费数+b.特殊处理)renew_stat,b.过期数 expire_stat,b.未激活数 noactive_stat,b.特殊处理 special_stat,CONCAT(CAST(round((((b.续费数+b.特殊处理)/(b.总数-b.未激活数)))*100,2) AS CHAR),'%')Renewal_ratio,
                    CONCAT(CAST(round(((b.过期数/(b.总数-b.未激活数)))*100,2) AS CHAR),'%')Loss_rate,
                    CONCAT(CAST(round(((b.未激活数/(b.总数)))*100,2) AS CHAR),'%')noactive_rate
                     from (
                    select custom_type,idx_data 统计月份,count(housing_num)总数,count(a.no_Renewal)待续费,count(isRenewal)续费数,count(isexpire)过期数,count(IF(company is not null and activation_day IS NULL, 1, NULL))未激活数,
                    count(IF(TIMESTAMPDIFF(MONTH, activation_day, end_day)>=2 and isRenewal is null and isexpire is null, 1, NULL))特殊处理
                    ,CONCAT(CAST(round((count(isRenewal)/count(*))*100,2) AS CHAR),'%')续费比
                    ,CONCAT(CAST(round((count(isexpire)/count(*))*100,2) AS CHAR),'%')流失率
                    from (
                    select if(isexpire is null and isRenewal is null and activation_day is not null,1,null)no_Renewal,t_Unpaid_count.*
                    from t_Unpaid_count)a
                    where housing_num is not null and a.custom_type="s" 
                    GROUP BY idx_data)b
                    UNION ALL
                    select b.custom_type,b.统计月份 idx_data,b.总数 sumcount,(b.待续费-b.特殊处理)no_Renewal,(b.续费数+b.特殊处理)renew_stat,b.过期数 expire_stat,b.未激活数 noactive_stat,b.特殊处理 special_stat,CONCAT(CAST(round((((b.续费数+b.特殊处理)/(b.总数-b.未激活数)))*100,2) AS CHAR),'%')Renewal_ratio,
                    CONCAT(CAST(round(((b.过期数/(b.总数-b.未激活数)))*100,2) AS CHAR),'%')Loss_rate,
                    CONCAT(CAST(round(((b.未激活数/(b.总数)))*100,2) AS CHAR),'%')noactive_rate
                     from (
                    select custom_type,idx_data 统计月份,count(housing_num)总数,count(a.no_Renewal)待续费,count(isRenewal)续费数,count(isexpire)过期数,count(IF(company is not null and activation_day IS NULL, 1, NULL))未激活数,
                    count(IF(TIMESTAMPDIFF(MONTH, activation_day, end_day)>=2 and isRenewal is null and isexpire is null, 1, NULL))特殊处理
                    ,CONCAT(CAST(round((count(isRenewal)/count(*))*100,2) AS CHAR),'%')续费比
                    ,CONCAT(CAST(round((count(isexpire)/count(*))*100,2) AS CHAR),'%')流失率
                    from (
                    select if(isexpire is null and isRenewal is null and activation_day is not null,1,null)no_Renewal,t_Unpaid_count.*
                    from t_Unpaid_count)a
                    where housing_num is not null and a.custom_type="m" 
                    GROUP BY idx_data)b                       
            '''
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Error get_stat_pay_first: {e}")
    finally:
        conn.close()


# 获取统计数据-试用期-查询
def get_stat_period_search(custom_type=None):
    conn = get_db_connection()
    lcustom_type=custom_type
    try:
        with conn.cursor() as cursor:


            sql = ("select b.custom_type,b.统计月份 idx_data,b.总数 sumcount,(b.待续费-b.特殊处理)no_Renewal,(b.续费数+b.特殊处理)renew_stat,b.过期数 expire_stat,b.未激活数 noactive_stat,b.特殊处理 special_stat,CONCAT(CAST(round((((b.续费数+b.特殊处理)/(b.总数-b.未激活数)))*100,2) AS CHAR),'%')Renewal_ratio,"
                "                            CONCAT(CAST(round(((b.过期数/(b.总数-b.未激活数)))*100,2) AS CHAR),'%')Loss_rate,"
                "                            CONCAT(CAST(round(((b.未激活数/(b.总数)))*100,2) AS CHAR),'%')noactive_rate"
                "                             from (select custom_type,idx_data 统计月份,count(housing_num)总数,count(a.no_Renewal)待续费,count(isRenewal)续费数,count(isexpire)过期数,count(IF(company is not null and activation_day IS NULL, 1, NULL))未激活数,"
                "                            count(IF(TIMESTAMPDIFF(MONTH, activation_day, end_day)>=2 and isRenewal is null and isexpire is null, 1, NULL))特殊处理"
                "                            ,CONCAT(CAST(round((count(isRenewal)/count(*))*100,2) AS CHAR),'%')续费比"
                "                            ,CONCAT(CAST(round((count(isexpire)/count(*))*100,2) AS CHAR),'%')流失率"
                "                            from (select if(isexpire is null and isRenewal is null and activation_day is not null,1,null)no_Renewal,t_Unpaid_count.*"
                "                            from t_Unpaid_count)a"
                "                            where housing_num is not null and a.custom_type=\""+custom_type+"\" GROUP BY idx_data)b order by b.统计月份 desc")

            
            # cursor.execute(sql, (str(custom_type),))
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Error get_stat_period_search: {e}")
    finally:
        conn.close()
