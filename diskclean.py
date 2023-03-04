
import os
import threading


class DiskClean:
    def __init__(self, path, limit=0.4):
        self.path = path
        self.limit = limit
        self.lock = threading.Lock()

    def check_space(self):
        """
        检查当前剩余空间是否小于限制
        """
        disk = os.statvfs(self.path)
        free_space = disk.f_frsize * disk.f_bavail
        total_space = disk.f_frsize * disk.f_blocks
        if free_space / total_space < self.limit - 0.1:
            return True
        else:
            return False

    def delete_oldest_file(self):
        """
        删除最早下载的文件
        """
        oldest_file = min(os.listdir(self.path), key=lambda x: os.path.getctime(os.path.join(self.path, x)))
        os.remove(os.path.join(self.path, oldest_file))

    def clean(self):
        """
        清理文件，直到剩余空间大于限制
        """
        with self.lock:
            while self.check_space():
                self.delete_oldest_file()
