import mysql.connector
import config


def get_db_connection():
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase,
    )
    return connection