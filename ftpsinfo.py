import ftpsdb
import ftplib
from dbconfig import MySQLInfo


class FtpServerInfo:
    def __init__(self, name, host, port, username, password, path):
        self.name = name
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.path = path


class FtpServerManager:
    def __init__(self):
        mysqlinfo = MySQLInfo().get_dbconfig_mysql()
        self.db = ftpsdb.FtpsDB(
            host=mysqlinfo.get('host'),
            port=mysqlinfo.get('port'),
            user=mysqlinfo.get('user'),
            passwd=mysqlinfo.get('password'),
            database='mrosync'
        )

    def add_server(self, name, host, port, username, password, path):
        try:
            # Check if server can be connected
            ftp = ftplib.FTP()
            ftp.connect(host, int(port))
            ftp.login(username, password)
            ftp.quit()
            # Add server to database
            self.db.insert(name, host, port, username, password, path)
            return True
        except Exception as err:
            print('add ftpserver Error:', err)
            return False

    def update_server(self, name, host, port, username, password, path):
        try:
            # Check if server can be connected
            ftp = ftplib.FTP()
            ftp.connect(host, int(port))
            ftp.login(username, password)
            ftp.quit()

            # Update server in database
            self.db.update(name, host, port, username, password, path)
            return True
        except Exception as err:
            print('update ftpserver Error:', err)
            return False

    def delete_server(self, name):
        self.db.delete(name)

    def get_server(self, name):
        return self.db.query_by_name(name)

    def get_all_servers(self):
        return self.db.query_all()

    def check_server(self, ftpinfo):
        try:
            ftp = ftplib.FTP()
            ftp.connect(ftpinfo.host, int(ftpinfo.port))
            ftp.login(ftpinfo.username, ftpinfo.password)
            ftp.quit()
            return True
        except Exception as err:
            print(err)
            return False

    def check_all_servers(self):
        servers = self.get_all_servers()
        unconnected_servers = []
        for server in servers:
            try:
                ftp = ftplib.FTP()
                ftp.connect(server.host, int(server.port))
                ftp.login(server.username, server.password)
                ftp.quit()
            except Exception as err:
                unconnected_servers.append({'ftp name': server.name, 'error': err})
        return unconnected_servers

    def get_connected_servers(self):
        """
        获取所有正常连接的ftp服务器列表
        """

        # 查询所有ftp服务器信息
        servers = self.get_all_servers()

        # 检查每个ftp服务器是否能连接，如果能连接则添加到结果列表中
        result = []
        for server in servers:
            host = server[1]
            port = server[2]
            username = server[3]
            password = server[4]
            try:
                print('Check FtpServer[()]'.format(host))
                ftp = ftplib.FTP()
                ftp.connect(host, int(port))
                ftp.login(username, password)
                result.append(server)
                ftp.quit()
            except Exception as err:
                print('error: ', err)
                continue
            return result
