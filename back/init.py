import mysql.connector
import config
from connections import get_db_connection

def init():
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword
    )
    cursor = connection.cursor()
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS `{config.DBdatabase}`;')
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `bases` (
            `id` int NOT NULL AUTO_INCREMENT,
            `first` varchar(255) DEFAULT NULL,
            `last` varchar(255) DEFAULT NULL,
            `email` varchar(255) DEFAULT NULL,
            `session` varchar(255) DEFAULT NULL,
            PRIMARY KEY (ID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `domains` (
            `id` int NOT NULL AUTO_INCREMENT,
            `url` TEXT DEFAULT NULL,
            `status` varchar(255) DEFAULT NULL,
            `session` varchar(255) DEFAULT NULL,
            `tempName` varchar(255) DEFAULT NULL,
            `template_id` int DEFAULT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `manifest` (
            `id` int NOT NULL AUTO_INCREMENT,
            `name` varchar(255) DEFAULT NULL,
            `type` varchar(255) DEFAULT NULL,
            PRIMARY KEY (ID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `materials` (
            `id` int NOT NULL AUTO_INCREMENT,
            `manifest` varchar(255) DEFAULT NULL,
            `data` longtext DEFAULT NULL,
            PRIMARY KEY (ID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `proxies` (
            `id` int NOT NULL AUTO_INCREMENT,
            `ip` varchar(255) DEFAULT NULL,
            `port` varchar(255) DEFAULT NULL,
            `status` varchar(255) DEFAULT NULL,
            `session` varchar(255) DEFAULT NULL,
            PRIMARY KEY (ID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `sessions` (
            `id` int NOT NULL AUTO_INCREMENT,
            `name` varchar(255) DEFAULT NULL,
            PRIMARY KEY (ID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `smtps` (
            `id` int NOT NULL AUTO_INCREMENT,
            `server` varchar(255) DEFAULT NULL,
            `port` varchar(255) DEFAULT NULL,
            `email` varchar(255) DEFAULT NULL,
            `password` varchar(255) DEFAULT NULL,
            `status` varchar(255) DEFAULT NULL,
            `session` varchar(255) DEFAULT NULL,
            PRIMARY KEY (ID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `templates` (
            `id` int NOT NULL AUTO_INCREMENT,
            `maintmp` int DEFAULT NULL,
            `template` longtext DEFAULT NULL,
            `froms` longtext DEFAULT NULL,
            `subject` longtext DEFAULT NULL,
            `status` varchar(255) DEFAULT NULL,
            `session` varchar(255) DEFAULT NULL,
            `htmlbodies` longtext DEFAULT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ''')
    cursor.execute( '''
            CREATE TABLE IF NOT EXISTS `temp` (
            `id` int NOT NULL AUTO_INCREMENT,
            `tempName` varchar(255) DEFAULT NULL,
            `status` varchar(255) DEFAULT NULL,
            `session` varchar(255) DEFAULT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `tokens` (
            `id` int NOT NULL AUTO_INCREMENT,
            `user` varchar(255) DEFAULT NULL,
            `token` varchar(255) DEFAULT NULL,
            PRIMARY KEY (ID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `users` (
            `id` int NOT NULL AUTO_INCREMENT,
            `name` varchar(255) DEFAULT NULL,
            `password` varchar(255) DEFAULT NULL,
            PRIMARY KEY (ID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `logs` (
        `id` int NOT NULL AUTO_INCREMENT,
        `TEXT` longtext DEFAULT NULL,
        `type` varchar(255) DEFAULT NULL,
        `session` varchar(255) DEFAULT NULL,
        `status` varchar(255) DEFAULT NULL,
        `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (ID)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `imaps` (
        `id` int NOT NULL AUTO_INCREMENT,
        `server` varchar(255) DEFAULT NULL,
        `port` varchar(255) DEFAULT NULL,
        `email` varchar(255) DEFAULT NULL,
        `password` varchar(255) DEFAULT NULL,
        `status` varchar(255) DEFAULT NULL,
        `session` varchar(255) DEFAULT NULL,
        PRIMARY KEY (ID)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS  `settings` (
        `session` VARCHAR(255) NOT NULL,
        `type` VARCHAR(255) NOT NULL,
        `data` INT,
        PRIMARY KEY (session, type)
    );
    ''')


def create_user(password='privatemailer'):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f'''
        INSERT INTO `users` (`name`, `password`)
        SELECT 'admin', '{password}'
        WHERE NOT EXISTS (SELECT 1 FROM `users` WHERE `name` = 'admin');
    ''')
    connection.commit()
