
import pymysql


class DLFilesLog:
    def __init__(self, ip, port, username, password, database):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.db = database
        self.conn = self.connect()
        self.create_database()
        self.create_table()

    def connect(self):
        # 连接到数据库
        conn = pymysql.connect(
            host=self.ip,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.db,
            charset='utf8mb4'
        )
        return conn

    def create_database(self):
        # create database if not exists
        cursor = self.conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db}")
        self.conn.commit()

    def create_table(self):
        # 如果表不存在则创建表
        cursor = self.conn.cursor()
        table_sql = '''
        CREATE TABLE IF NOT EXISTS mrofileslog (
            id INT(11) NOT NULL AUTO_INCREMENT,
            ftp_name VARCHAR(50) NOT NULL,
            file_dir VARCHAR(100) NOT NULL,
            file_name VARCHAR(100) NOT NULL,
            file_size BIGINT NOT NULL,
            download_time DATETIME NOT NULL,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        '''
        cursor.execute(table_sql)
        self.conn.commit()

    def insert_log(self, ftp_name, file_dir, file_name, file_size, download_time):
        # 将下载的文件信息插入到表中
        cursor = self.conn.cursor()
        insert_sql = '''
        INSERT INTO mrofileslog (ftp_name, file_dir, file_name, file_size, download_time)
        VALUES (%s, %s, %s, %s, %s)
        '''
        values = (ftp_name, file_dir, file_name, file_size, download_time)
        cursor.execute(insert_sql, values)
        self.conn.commit()

    def check_if_downloaded(self, ftp_name, file_dir, file_name):
        # 检查文件是否已经被下载
        cursor = self.conn.cursor()
        select_sql = '''
        SELECT * FROM mrofileslog
        WHERE ftp_name = %s AND file_dir = %s AND file_name = %s
        '''
        values = (ftp_name, file_dir, file_name)
        cursor.execute(select_sql, values)
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
