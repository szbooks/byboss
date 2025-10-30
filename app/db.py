import pymysql

from flask import current_app

def get_db_connection():
    return pymysql.connect(host=current_app.config['DB_HOST'],
                           user=current_app.config['DB_USER'],
                           password=current_app.config['DB_PASSWORD'],
                           db=current_app.config['DB_NAME'],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

def get_db_connection_read():
    return pymysql.connect(host=current_app.config['DB_HOST_READ'],
    # return pymysql.connect(host=current_app.config['DB_HOST_READ_DEV'],
                           user=current_app.config['DB_USER_READ'],
                           password=current_app.config['DB_PASSWORD_READ'],
                           db=current_app.config['DB_NAME_READ'],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)



def get_db_connection_w():
    return pymysql.connect(host=current_app.config['DB_HOST_W'],
                           user=current_app.config['DB_USER_W'],
                           password=current_app.config['DB_PASSWORD_W'],
                           db=current_app.config['DB_NAME_W'],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)



