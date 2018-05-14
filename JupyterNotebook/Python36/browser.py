# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2018-05-09 10:04

浏览器对象
"""
from selenium import webdriver


class Browser(object):
    """
    浏览器对象，基于selenium，单例模式，自动回收驱动对象。

    最新的selenium声称不支持PhantomJS了，考虑到服务器上运行的问题，这里使用2.53.6版本的selenium。
    使用之前，除了安装selenium（pip install selenium==2.53.6）之外，还需要安装PhantomJS，并配置到系统环境变量中。
    PhantomJS下载地址：http://phantomjs.org/download.html

    使用示例:
    with Browser() as browser:
        browser.get('https://www.baidu.com/')
    """

    def __enter__(self):
        self.browser = webdriver.PhantomJS(service_log_path='./log_file/browser.log')
        self.browser.viewportSize = {'width': 1366, 'height': 768}
        self.browser.maximize_window()
        return self.browser

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            self.browser.quit()
