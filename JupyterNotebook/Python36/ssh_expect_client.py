# -*- coding: utf-8 -*-
import pexpect


class SSHExpectClient(object):
    """
    使用pexpect封装的上下文管理器，用于登录服务器执行相关操作
    注：该方法不支持windows环境

    使用示例：
    ssh_conf = {
        'host': '192.168.206.91',
        'username': 'root',
        'password': 'axn#2017#913',
        'logfile': 'logfile.txt'
    }
    with SSHExpectClient(**ssh_conf) as sec:
        print('====>', sec.before.decode('utf-8'))
        sec.sendline('ls -lh')
        sec.expect(SSHExpectClient.PROMPT, timeout=5)
        print('====>', sec.before.decode('utf-8'))
    """

    PROMPT = ['# ', '$ ']

    def __init__(self, host, username, password, logfile=None):
        """
        初始化连接参数
        :param host: 主机地址
        :param username: 用户名
        :param password: 密码
        :param logfile: 指定日志文件，默认为None
        """
        self.host = host
        self.username = username
        self.password = password
        self.logfile = logfile

    def __enter__(self):
        """
        进入上下文管理器时执行初始化连接
        :return: 操作句柄
        """
        command = 'ssh {0}@{1}'.format(self.username, self.host)
        self.child = pexpect.spawn(
            command,
            logfile=open(self.logfile, 'wb') if self.logfile else None
        )
        index = self.child.expect(['password:', 'continue connecting(yes/no)?'], timeout=5)
        if index == 0:
            self.child.sendline(self.password)
            self.child.expect(self.PROMPT)
        elif index == 1:
            self.child.sendline('yes')
            self.child.expect('password:', timeout=5)
            self.child.sendline(self.password)
            self.child.expect(self.PROMPT)
        else:
            raise Exception(self.child.before)
        return self.child

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        离开上下文管理器时关闭连接
        :param exc_type: exc_type
        :param exc_val: exc_val
        :param exc_tb: exc_tb
        :return: 无
        """
        self.child.close()
