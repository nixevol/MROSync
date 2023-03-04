import threading

from diskclean import DiskClean
from ftpsinfo import FtpServerManager
from dbconfig import MySQLInfo

class Control:
    def __init__(self):
        self.mysql = MySQLInfo
        self.ftp = FtpServerManager
        self.disk = DiskClean
        self.status = False

    def start(self):
        if self.status:
            print("服务已经在运行中...")
        else:
            self.status = True
            print("服务开始运行...")
            # 启动 FTP 服务器状态检查线程
            ftp_thread = threading.Thread(target=self.ftp_check)
            ftp_thread.setDaemon(True)
            ftp_thread.start()
            # 启动储存空间检查线程
            disk_thread = threading.Thread(target=self.disk_check)
            disk_thread.setDaemon(True)
            disk_thread.start()

    def stop(self):
        if not self.status:
            print("服务已经停止运行...")
        else:
            self.status = False
            print("服务停止运行...")

    def mysql_edit(self):
        host = input("请输入MySQL服务器地址：")
        port = input("请输入MySQL端口：")
        user = input("请输入MySQL账号：")
        password = input("请输入MySQL密码：")
        self.mysql().edit_dbconfig_mysql(host=host, port=port, username=user, password=password)

    def mysql_show(self):
        print(self.mysql().get_dbconfig_mysql())

    def ftp_add(self):
        ftpname = input("请输入FTP服务器名称：")
        address = input("请输入FTP服务器地址：")
        port = input("请输入FTP服务器端口：")
        account = input("请输入FTP服务器账号：")
        password = input("请输入FTP服务器密码：")
        scanpath = input("请输入FTP服务器扫描路径：")
        self.ftp().add_server(ftpname, address, port, account, password, scanpath)

    def ftp_update(self):
        ftpname = input("请输入FTP服务器名称：")
        address = input("请输入FTP服务器地址：")
        port = input("请输入FTP服务器端口：")
        account = input("请输入FTP服务器账号：")
        password = input("请输入FTP服务器密码：")
        scanpath = input("请输入FTP服务器扫描路径：")
        self.ftp().update_server(ftpname, address, port, account, password, scanpath)

    def ftp_delete(self):
        ftpname = input("请输入要删除的FTP服务器名称：")
        self.ftp().delete_server(ftpname)

    def ftp_check(self):
        ftp_list = self.ftp().get_all_servers()
        error_list = []
        for ftp in ftp_list:
            if not self.ftp().check_server(ftp):
                error_list.append(ftp)
        if error_list:
            print(f"以下FTP服务器连接错误：{error_list}")
        else:
            print("所有FTP服务器连接正常")

    def ftp_getall(self):
        ftp_list = self.ftp().get_all_servers()
        for ftp in ftp_list:
            print(f"{ftp.id} {ftp.name} {ftp.address} {ftp.port} {ftp.account} {ftp.password} {ftp.scanpath}")

    def disk_check(self):
        self.disk('/sync/')
