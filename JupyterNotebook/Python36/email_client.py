# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@zjaisino.com
@created_time: 2018-01-15 09:18
"""
import logging
import smtplib
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


class EmailClient(object):
    """
    发送邮件
    """

    def __init__(self, mail_title, mail_body, mail_user, mail_pwd, mailto_list,
                 server_host, server_type, mail_type='html', charset='gbk'):
        self.mail_title = mail_title
        self.mail_body = mail_body
        self.mail_user = mail_user
        self.mail_pwd = mail_pwd
        self.mailto_list = mailto_list
        self.server_host = server_host
        self.server_type = server_type
        self.server_port = self.__init_server_port()
        self.mail_type = mail_type
        self.charset = charset

    def __init_server_port(self):
        """
        初始化邮件服务器信息
        :return: 服务器信息
        """
        server_type = self.server_type.lower()
        if server_type == 'smtp':
            return 465
        elif server_type == 'pop3':
            return 995
        elif server_type == 'imap':
            return 993
        else:
            raise Exception('[EMAIL ERROR] Invalid email server-type! {0}'.format(server_type))

    def __do_send_action(self, s, msg):
        """
        执行发送操作
        :param s: 服务器连接
        :param msg: 邮件内容实例
        :return: 执行结果
        """
        try:
            s.sendmail(self.mail_user, self.mailto_list, msg.as_string())
            s.quit()
            s.close()
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def send(self):
        # 创建一个实例
        msg = MIMEText(self.mail_body, _subtype=self.mail_type, _charset=self.charset)
        # 设置邮件主题
        msg['Subject'] = self.mail_title
        # 设置发件人
        msg['From'] = self.mail_user
        # 设置收件人
        msg['To'] = ';'.join(self.mailto_list)
        # 获取服务器连接
        s = smtplib.SMTP_SSL(self.server_host, self.server_port)
        s.login(self.mail_user.split('@')[0], self.mail_pwd)
        # 发送邮件
        status = self.__do_send_action(s, msg)
        return status
