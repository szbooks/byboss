import datetime

from app.db import get_db_connection


# 读取发票列表
def get_receipts():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT receipt.*,t_account.username as todo_account_name FROM 
                (
                SELECT t_receipt.*,t_account.username as create_account_name FROM t_receipt 
                LEFT JOIN t_account ON t_account.id = t_receipt.create_account_id
                ) AS receipt
                LEFT JOIN t_account ON t_account.id = receipt.todo_account_id 
                ORDER BY receipt.create_datetime desc 
            '''
            cursor.execute(sql)
            receipts = cursor.fetchall()
            return receipts
    except Exception as e:
        print(f"Error get_receipts: {e}")
    finally:
        conn.close()


# 读取发票列表
def get_receipts_by_status(status,company_info=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 初始化条件列表和参数列表
            sql_conditions = ["1=1"]  # 默认条件
            query_params = []

            # 添加状态过滤条件
            if status not in (None, ''):
                sql_conditions.append("receipt.status = %s")
                query_params.append(status)

            # 添加公司信息过滤条件
            if company_info not in (None, ''):
                sql_conditions.append("(receipt.company_id = %s OR receipt.invoice_head = %s)")
                query_params.extend([company_info, company_info])  # 添加两个参数

            # 构建 SQL 查询
            sql = '''
                SELECT receipt.*, t_account.username AS todo_account_name 
                FROM (
                    SELECT t_receipt.*, t_account.username AS create_account_name 
                    FROM t_receipt
                    LEFT JOIN t_account ON t_account.id = t_receipt.create_account_id
                ) AS receipt
                LEFT JOIN t_account ON t_account.id = receipt.todo_account_id
                WHERE ''' + " AND ".join(sql_conditions) + " ORDER BY receipt.id DESC"

            try:
                # 执行查询
                cursor.execute(sql, query_params)
                receipts = cursor.fetchall()
                return receipts
            except Exception as e:
                print(f"Error get_receipts_by_status: {e}")
                raise
    except Exception as e:
        print(f"Error get_receipts_by_status: {e}")
    finally:
        conn.close()


# 读取发票详情
def get_receipt(receipt_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT * FROM t_receipt
                WHERE id = %s
            '''
            cursor.execute(sql, receipt_id)
            receipt = cursor.fetchone()
            return receipt
    except Exception as e:
        print(f"Error get_receipt: {e}")
    finally:
        conn.close()


# 更新发票状态
def update_receipt_status(receipt_id, company_id, phone, price, invoice_head, tax_id, khh, bank_account, addr, remark, status, todo_remark=None, todo_account_id=None, todo_datetime=None):
    conn = get_db_connection()

    # update_receipt_status(receipt_id, company_id, phone, price, remark, 2, todo_remark, current_user_id, current_time)
    try:
        with conn.cursor() as cursor:
            if status==1:
                sql = '''
                                UPDATE t_receipt
                                SET status = %s, company_id= %s,phone= %s,price= %s,remark= %s,invoice_head = %s,tax_id = %s,addr = %s,khh = %s,bank_account = %s
                                WHERE id = %s
                            '''
                cursor.execute(sql, (status,  company_id, phone, price, remark, invoice_head, tax_id, addr, khh, bank_account, receipt_id))
                conn.commit()
            else:

                sql = '''
                    UPDATE t_receipt
                    SET status = %s, todo_remark = %s, todo_account_id = %s, todo_datetime = %s, company_id= %s,phone= %s,price= %s,remark= %s,invoice_head = %s,tax_id = %s,addr = %s,khh = %s,bank_account = %s
                    WHERE id = %s
                '''
                cursor.execute(sql, (status, todo_remark, todo_account_id, todo_datetime, company_id, phone, price, remark, invoice_head, tax_id, addr, khh, bank_account, receipt_id))
                conn.commit()
    except Exception as e:
        print(f"Error update_receipt_status: {e}")
    finally:
        conn.close()


# 申请新发票
def add_new_receipt(company_id, phone, price, invoice_head, tax_id, khh, bank_account, addr, remark, create_account_id, todo_account_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                INSERT INTO t_receipt (company_id, phone, price, invoice_head, tax_id, khh, bank_account, addr,remark, status, create_account_id, create_datetime, todo_account_id)
                VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s)
            '''
            status = 1
            current_time = datetime.datetime.now()
            cursor.execute(sql, (company_id, phone, price, invoice_head, tax_id, khh, bank_account, addr, remark, status, create_account_id, current_time, todo_account_id))
            conn.commit()
            # 获取插入记录的ID
            return cursor.lastrowid
    except Exception as e:
        print(f"Error add_new_receipt: {e}")
    finally:
        conn.close()


def edit_receipt(company_id, phone, price, invoice_head, tax_id, khh, bank_account, addr, remark, create_account_id, todo_account_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                INSERT INTO t_receipt (company_id, phone, price, invoice_head, tax_id, khh, bank_account, addr,remark, status, create_account_id, create_datetime, todo_account_id)
                VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s)
            '''
            status = 1
            current_time = datetime.datetime.now()
            cursor.execute(sql, (company_id, phone, price, invoice_head, tax_id, khh, bank_account, addr, remark, status, create_account_id, current_time, todo_account_id))
            conn.commit()
            # 获取插入记录的ID
            return cursor.lastrowid
    except Exception as e:
        print(f"Error add_new_receipt: {e}")
    finally:
        conn.close()


# 发票查询-新增和处理页面，按公司
def company_receipts_filter(company_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                select * from t_receipt where company_id=%s and (invoice_head is not null or tax_id is not null or khh is not null or bank_account is not null or addr is not null) and 
(invoice_head <>"" or tax_id <>"" or khh <>"" or bank_account <>"" or addr <>"") ORDER BY create_datetime desc;
            '''
            cursor.execute(sql, (company_id,))
            company = cursor.fetchall()
            if company:
                complete_fields = {'company_id':company_id,'invoice_head': None, 'tax_id': None, 'khh': None, 'bank_account': None, 'addr': None, 'phone': None}

                # 如果查询结果不为空，则遍历每一行数据，填充不为空的字段

                for row in company:
                    # 假设表结构为 (id, company_id, invoice_head, tax_id, khh, bank_account, addr, create_datetime, ...)
                    # 根据实际情况调整索引
                    invoice_head = row.get('invoice_head')
                    tax_id = row.get('tax_id')
                    khh = row.get('khh')
                    bank_account = row.get('bank_account')
                    addr = row.get('addr')
                    phone = row.get('phone')

                    # 检查每个字段是否不为空，并填充到 complete_fields 中
                    if invoice_head is not None and invoice_head.strip() != "":
                        complete_fields['invoice_head'] = invoice_head.strip()
                    if tax_id is not None and tax_id.strip() != "":
                        complete_fields['tax_id'] = tax_id.strip()
                    if khh is not None and khh.strip() != "":
                        complete_fields['khh'] = khh.strip()
                    if bank_account is not None and bank_account.strip() != "":
                        complete_fields['bank_account'] = bank_account.strip()
                    if addr is not None and addr.strip() != "":
                        complete_fields['addr'] = addr.strip()
                    if phone is not None and phone.strip() != "":
                        complete_fields['phone'] = phone.strip()

            # company = cursor.fetchall()
            # print("Query result:", company)
            # for row in company:



            return complete_fields
    except Exception as e:
        print(f"Error in company_receipts_filter: {e}")
    finally:
        conn.close()

# 发票查询-新增和处理页面，按开票公司
def head_receipts_filter(head):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                select * from t_receipt where invoice_head=%s and (invoice_head is not null or tax_id is not null or khh is not null or bank_account is not null or addr is not null) and 
(invoice_head <>"" or tax_id <>"" or khh <>"" or bank_account <>"" or addr <>"") ORDER BY create_datetime desc;
            '''
            cursor.execute(sql, (head,))
            heads = cursor.fetchall()

            if heads:
                complete_fields = {'invoice_head': None, 'tax_id': None, 'khh': None, 'bank_account': None, 'addr': None,'phone': None}

                # 如果查询结果不为空，则遍历每一行数据，填充不为空的字段

                for row in heads:
                    # 假设表结构为 (id, company_id, invoice_head, tax_id, khh, bank_account, addr, create_datetime, ...)
                    # 根据实际情况调整索引
                    invoice_head = row.get('invoice_head')
                    tax_id = row.get('tax_id')
                    khh = row.get('khh')
                    bank_account = row.get('bank_account')
                    addr = row.get('addr')
                    phone = row.get('phone')

                    # 检查每个字段是否不为空，并填充到 complete_fields 中
                    if invoice_head is not None and invoice_head.strip() != "":
                        complete_fields['invoice_head'] = invoice_head.strip()
                    if tax_id is not None and tax_id.strip() != "":
                        complete_fields['tax_id'] = tax_id.strip()
                    if khh is not None and khh.strip() != "":
                        complete_fields['khh'] = khh.strip()
                    if bank_account is not None and bank_account.strip() != "":
                        complete_fields['bank_account'] = bank_account.strip()
                    if addr is not None and addr.strip() != "":
                        complete_fields['addr'] = addr.strip()
                    if phone is not None and phone.strip() != "":
                        complete_fields['phone'] = phone.strip()

            return complete_fields
    except Exception as e:
        print(f"Error in head_receipts_filter: {e}")
    finally:
        conn.close()

def partner_receipts_filter(Partner):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                select * from t_company c join t_receipt r on c.company_id=r.company_id where c.source=%s and (r.invoice_head is not null or r.tax_id is not null or r.khh is not null or r.bank_account is not null or r.addr is not null) and 
(r.invoice_head <>"" or r.tax_id <>"" or r.khh <>"" or r.bank_account <>"" or r.addr <>"") ORDER BY r.create_datetime desc limit 10;
            '''
            cursor.execute(sql, (Partner,))
            company = cursor.fetchall()
            if company:
                complete_fields = {'company_id':None,'invoice_head': None, 'tax_id': None, 'khh': None, 'bank_account': None, 'addr': None, 'phone': None}

                # 如果查询结果不为空，则遍历每一行数据，填充不为空的字段

                for row in company:
                    # 假设表结构为 (id, company_id, invoice_head, tax_id, khh, bank_account, addr, create_datetime, ...)
                    # 根据实际情况调整索引
                    company_id = row.get('company_id')
                    invoice_head = row.get('invoice_head')
                    tax_id = row.get('tax_id')
                    khh = row.get('khh')
                    bank_account = row.get('bank_account')
                    addr = row.get('addr')
                    phone = row.get('phone')

                    # 检查每个字段是否不为空，并填充到 complete_fields 中
                    if company_id is not None and company_id.strip() != "":
                        complete_fields['company_id'] = company_id.strip()
                    if invoice_head is not None and invoice_head.strip() != "":
                        complete_fields['invoice_head'] = invoice_head.strip()
                    if tax_id is not None and tax_id.strip() != "":
                        complete_fields['tax_id'] = tax_id.strip()
                    if khh is not None and khh.strip() != "":
                        complete_fields['khh'] = khh.strip()
                    if bank_account is not None and bank_account.strip() != "":
                        complete_fields['bank_account'] = bank_account.strip()
                    if addr is not None and addr.strip() != "":
                        complete_fields['addr'] = addr.strip()
                    if phone is not None and phone.strip() != "":
                        complete_fields['phone'] = phone.strip()

            return complete_fields
    except Exception as e:
            print(f"Error in head_receipts_filter: {e}")
    finally:
            conn.close()




def del_receipt_record(receipt_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                 DELETE from t_receipt where id=%s
             '''
            cursor.execute(sql, (receipt_id,))
            conn.commit()
            return "success"
    except Exception as e:
        print(f"Error in company_receipts_filter: {e}")
    finally:
        conn.close()
