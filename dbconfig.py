
import os
import configparser
import pymysql


class MySQLInfo:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = os.path.join(os.getcwd(), 'config', 'dbinfo.ini')
        self.config.read(self.config_path, encoding='utf-8')
        if not os.path.exists(self.config_path):
            if not os.path.exists(os.path.join(os.getcwd(), 'config')):
                os.makedirs(os.path.join(os.getcwd(), 'config'))
                f = open(self.config_path, 'a', encoding='utf-8')
                f.close()

    def edit_dbconfig_mysql(self, host='localhost', port=3306, username='root', password=''):
        if not self.config.has_section('MySQL'):
            self.config.add_section('MySQL')

        if host is not None:
            self.config.set('MySQL', 'host', host)
        if port is not None:
            self.config.set('MySQL', 'port', str(port))
        if username is not None:
            self.config.set('MySQL', 'username', username)
        if password is not None:
            self.config.set('MySQL', 'password', password)

        try:
            conn = pymysql.connect(host=host, port=int(port), user=username, password=password)
            conn.close()
            print('success')
            with open(self.config_path, 'w', encoding='utf-8') as cfg:
                self.config.write(cfg)
            return True
        except Exception as err:
            print('配置保存失败，请检查数据库()信息，错误原因：'.format(host), err)
            return False

    def get_dbconfig_mysql(self):
        mysql_info = {
            'option': 'MySQL',
            'host': self.config.get('MySQL', 'host'),
            'port': int(self.config.get('MySQL', 'port')),
            'user': self.config.get('MySQL', 'username'),
            'password': self.config.get('MySQL', 'password')
        }
        return mysql_info
