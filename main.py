import control

if __name__ == '__main__':
    print("欢迎使用FTP监控程序")
    print("指令说明：")
    print("START: 启动服务")
    print("STOP: 停止服务")
    print("MySQL.edit: 修改数据库信息")
    print("MySQL.show: 查看数据库信息")
    print("FTP.add: 添加FTP服务器信息")
    print("FTP.update: 修改FTP服务器信息")
    print("FTP.del: 删除FTP服务器信息")
    print("FTP.check: 返回FTP服务器错误列表")
    print("FTP.getall: 返回所有的FTP服务器信息")
    print("DISK.info: 返回当前储存空间使用情况")
    print("DISK.clean: 清理储存空间直至剩余40%")
    print("exit: 退出指令控制台，程序后台运行")

    while True:
        command = input("请输入指令：")
        if command == "START":
            control.Control().start()
        elif command == "STOP":
            control.Control().stop()
        elif command == "MySQL.edit":
            control.Control().mysql_edit()
        elif command == "MySQL.show":
            control.Control().mysql_show()
        elif command == "FTP.add":
            control.Control().ftp_add()
        elif command == "FTP.update":
            control.Control().ftp_update()
        elif command == "FTP.del":
            control.Control().ftp_delete()
        elif command == "FTP.check":
            control.Control().ftp_check()
        elif command == "FTP.getall":
            control.Control().ftp_getall()
        elif command == "DISK.clean":
            control.Control().disk_check()
        elif command == "exit":
            print("程序后台运行")
            break
        else:
            print("无效指令，请重新输入！")
