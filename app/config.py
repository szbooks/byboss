import os

# --- 数据库配置 ---
DB_HOST = 'rm-bp1frx74xka4hr77vvo.mysql.rds.aliyuncs.com'
# DB_HOST = 'rm-bp1frx74xka4hr77v.mysql.rds.aliyuncs.com'
DB_PORT = 3306
DB_USER = 'jonny'
DB_PASSWORD = 'kuang123BYPMS'
DB_NAME = 'dh_support'

DB_HOST_READ = 'rr-bp102335g97l5k6318o.mysql.rds.aliyuncs.com'
# DB_HOST_READ_DEV = 'rr-bp102335g97l5k631.mysql.rds.aliyuncs.com'
DB_PORT_READ = 3306
DB_USER_READ = 'jonny'
DB_PASSWORD_READ = 'kuang123BYPMS'
DB_NAME_READ = 'dh_short_rent'



DB_HOST_W = 'rm-bp18b7brvsxna6376yo.mysql.rds.aliyuncs.com'
# DB_HOST_READ_DEV = 'rr-bp102335g97l5k631.mysql.rds.aliyuncs.com'
DB_PORT_W = 3306
DB_USER_W = 'jonny'
DB_PASSWORD_W = 'kuang123BYPMS'
DB_NAME_W = 'dh_short_rent'






# --- OSS配置 ---
SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key'

# --- 显示 ---
PAGE_RECORD_NUM = 25

# --- 微信支付 ---

# wx域名
wx_domain = ' https://api.mch.weixin.qq.com/'


# 替换为你的API V3密钥
api_v3_key = 'your_api_v3_key_here'

# 替换为你的私钥路径
private_key_path = 'E:/项目/宝寓/微信支付接口相关/WXCertUtil/cert/apiclient_key.pem'

#获取微信投诉列表
url = '/v3/merchant-service/complaints-v2'


#（仅能重置未开通房态同步，且开启了订单同步的账号）
initial_order_url = 'https://www.bypms.cn/admin/company/account/reset_contract?id='

#如果重置的账号有历史订单无法重置，使用以下网址强制重置
initial_order_gnoreHistory_url = 'https://www.bypms.cn/admin/company/account/reset_contract?ignoreHistory=1&id='

#图片文件存储路径
UPLOAD_FOLDER = r'F:\pic\vip_refund'








