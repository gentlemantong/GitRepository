# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2018-05-09 10:04

浏览器对象
"""
import threading

from selenium import webdriver


class Browser(object):
    """
    浏览器对象，基于selenium，单例模式，多线程安全，自动回收驱动对象。

    最新的selenium声称不支持PhantomJS了，考虑到服务器上运行的问题，这里使用2.53.6版本的selenium。
    使用之前，除了安装selenium（pip install selenium==2.53.6）之外，还需要安装PhantomJS，并配置到系统环境变量中。
    PhantomJS下载地址：http://phantomjs.org/download.html

    使用示例:
    b = Browser()
    b.browser.get('https://www.baidu.com/')
    """

    _mutex = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """
        实例化方法
        :param args: 参数
        :param kwargs: 关键字
        :return: 实例
        """
        if not hasattr(Browser, '_instance'):
            with Browser._mutex:
                if not hasattr(Browser, '_instance'):
                    Browser._instance = object.__new__(cls)
                    Browser._instance.browser = webdriver.PhantomJS()
                    Browser._instance.browser.viewportSize = {'width': 1366, 'height': 768}
                    Browser._instance.browser.maximize_window()
        return Browser._instance

    def __del__(self):
        """
        析构方法
        :return: 无
        """
        if hasattr(self, 'browser'):
            with Browser._mutex:
                if hasattr(self, 'browser'):
                    self.browser.quit()
