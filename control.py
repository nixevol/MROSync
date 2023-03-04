import threading
import time

from ftpsync import FTPSync
from diskclean import DiskClean
from ftpsinfo import FtpServerManager
from dbconfig import MySQLInfo


class FTPThread(threading.Thread):
    """自定义线程类"""

    def __init__(self, ftp_server):
        threading.Thread.__init__(self)
        self.ftp_server = ftp_server
        self.FTPSync = FTPSync(ftp_name=ftp_server.name, ftp_ip=ftp_server.host, ftp_port=int(ftp_server.port),
                               ftp_user=ftp_server.username, ftp_password=ftp_server.passwd, local_dir=ftp_server.path)
        self.stop_flag = threading.Event()  # 初始化停止标志

    def run(self):
        print(f"{self.ftp_server} 线程启动")
        while not self.stop_flag.is_set():
            try:
                self.FTPSync.start()
            except Exception as e:
                print(f"{self.ftp_server} 下载出错：{e}")
            time.sleep(60)
        print(f"{self.ftp_server} 线程停止")


class Control:
    def __init__(self):
        self.mysql = MySQLInfo
        self.ftp = FtpServerManager
        self.disk = DiskClean
        self.status = False
        self.threads = []  # 存储线程对象
        self.is_started = False  # 是否已经启动标志
        self.stop_flag = False  # 停止标志

    def start(self):
        """启动FTP同步"""
        if self.is_started:
            print("线程已经启动")
            return
        print("开始启动线程")
        ftp_servers = self.ftp().get_connected_servers()
        for ftp_server in ftp_servers:
            thread = FTPThread(ftp_server)
            thread.start()
            self.threads.append(thread)
        self.is_started = True
        print("线程已经全部启动")

    def stop(self):
        """停止FTP同步"""
        if not self.is_started:
            print("线程已经关闭")
            return
        print("开始停止线程")
        self.stop_flag = True
        for thread in self.threads:
            thread.stop_flag.set()  # 设置停止标志
        for thread in self.threads:
            thread.join()  # 等待线程结束
        self.threads.clear()
        self.is_started = False
        self.stop_flag = False
        print("线程已经全部停止")

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
