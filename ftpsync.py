
import os
import time
from ftplib import FTP
from dlfileslog import DLFilesLog
from diskclean import DiskClean
from dbconfig import MySQLInfo


class FTPSync:
    def __init__(self, ftp_name, ftp_ip, ftp_port, ftp_user, ftp_password, local_dir):
        self.ftp_name = ftp_name
        self.ftp_ip = ftp_ip
        self.ftp_port = int(ftp_port)
        self.ftp_user = ftp_user
        self.ftp_password = ftp_password
        self.local_dir = os.path.join(local_dir, ftp_name)
        self.scan_dir = local_dir

    def start(self):
        # 连接FTP服务器
        ftp = FTP()
        ftp.connect(self.ftp_ip, self.ftp_port)
        ftp.login(self.ftp_user, self.ftp_password)
        ftp.cwd('/mrodata')

        # 获取FTP服务器中所有MRO文件
        files = ftp.nlst()

        # 遍历MRO文件
        for file in files:
            file_name = os.path.basename(file)
            mysqlinfo = MySQLInfo().get_dbconfig_mysql()
            # 检查是否已经下载过
            dl_files_log = DLFilesLog(
                ip=mysqlinfo.get('host'),
                port=mysqlinfo.get('port'),
                username=mysqlinfo.get('user'),
                password=mysqlinfo.get('password'),
                database='mrosync'
            )
            if dl_files_log.check_if_downloaded(self.ftp_name, self.local_dir, file_name):
                continue
            # 检查本地存储空间是否足够
            disk_clean = DiskClean(self.scan_dir)
            if not disk_clean.check_space():
                disk_clean.delete_oldest_file()

            # 检查是否为ZIP文件
            if not file.endswith('.zip'):
                continue
            # 下载文件
            ftp.voidcmd('TYPE I')
            file_size = ftp.size(file)
            local_file_path = os.path.join(self.local_dir, file_name)
            with open(local_file_path, 'wb') as f:
                ftp.retrbinary('RETR ' + file, f.write)

            # 记录文件下载记录
            dl_files_log.insert_log(self.ftp_name, file_name, local_file_path, file_size, time.time())

            # 向后台提交下载完成指令
            # TODO: submit download complete command to backend
            print(f"Downloaded file {file_name} from {self.ftp_ip}")

        ftp.quit()
