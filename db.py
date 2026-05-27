import pymysql


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "anksoonamoon",
    "db": "fabric_store_2",
}


conn = pymysql.connect(**DB_CONFIG)
