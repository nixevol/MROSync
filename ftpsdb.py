
import pymysql


class FtpsDB:
    def __init__(self, host, port, user, passwd, database):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.passwd,
                database=self.database
            )
            self.cursor = self.conn.cursor()
            self.create_database()
            self.create_table()
        except pymysql.connect.Error as err:
            print("Error while connecting to MySQL", err)
        except Exception as err:
            print("Error ", err)

    def create_database(self):
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        except pymysql.connect.Error as err:
            print("Error while creating database: ", err)

    def create_table(self):
        try:
            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS ftpsinfo ("
                f"id INT(11) NOT NULL AUTO_INCREMENT,"
                f"name VARCHAR(255) NOT NULL,"
                f"host VARCHAR(255) NOT NULL,"
                f"port INT(11) NOT NULL,"
                f"user VARCHAR(255) NOT NULL,"
                f"passwd VARCHAR(255) NOT NULL,"
                f"path VARCHAR(255) NOT NULL,"
                f"PRIMARY KEY (id)"
                f") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"
            )
        except pymysql.connect.Error as err:
            print("Error while creating table: ", err)
        except Exception as err:
            print("Error ", err)

    def execute_query(self, sql, values=None, commit=False):
        self.connect()
        try:
            self.cursor.execute(sql, values)
            if commit:
                self.conn.commit()
            return self.cursor
        except pymysql.connect.Error as err:
            print("Error while executing query: ", err)
        except Exception as err:
            print("Error ", err)

    def query_all(self):
        sql = "SELECT * FROM ftpsinfo"
        result = self.execute_query(sql).fetchall()
        return result

    def query_by_name(self, name):
        sql = "SELECT * FROM ftpsinfo WHERE name = %s"
        result = self.execute_query(sql, (name,)).fetchall()
        return result

    def insert(self, name, host, port, user, passwd, path):
        sql = "INSERT INTO ftpsinfo (name, host, port, user, passwd, path) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (name, host, port, user, passwd, path)
        self.execute_query(sql, values, commit=True)

    def update(self, name, host, port, user, passwd, path):
        sql = "UPDATE ftpsinfo SET host=COALESCE(%s, host), port=COALESCE(%s, port), user=COALESCE(%s, user), " \
              "passwd=COALESCE(%s, passwd), path=COALESCE(%s, path) WHERE name=%s"
        values = (host, port, user, passwd, path, name)
        self.execute_query(sql, values, commit=True)

    def delete(self, name):
        sql = "DELETE FROM ftpsinfo WHERE name=%s"
        values = (name,)
        self.execute_query(sql, values, commit=True)
