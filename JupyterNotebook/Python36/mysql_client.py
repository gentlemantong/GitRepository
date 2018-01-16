# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@zjaisino.com
@created_time: 2018-01-04 13:09
"""
import logging

import pymysql

logger = logging.getLogger(__name__)


class MySQLClient(object):
    """
    MySQL相关方法
    所有的连接均为短连接，用完就关闭
    """

    @staticmethod
    def __init_client(db_config):
        """
        初始化MySQL连接
        :param db_config: 连接参数
        :return: 无
        """
        client = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            passwd=db_config['passwd'],
            db=db_config['db'],
            charset=db_config['charset']
        )
        if client.cursor():
            return client
        else:
            raise Exception('[MySQL连接失败] [%s:%s]' % (db_config['host'], db_config['port']))

    @classmethod
    def __execute(cls, db_config, db_query, params, many=False):
        """
        update、insert类操作
        :param db_config: 连接参数
        :param db_query: SQL语句
        :param params: 其他参数
        :param many: 是否一次执行多个
        :return: 无
        """
        if many and not params:
            raise Exception('[MySQL执行参数错误] Invalid params: %s' % params)
        client = cls.__init_client(db_config)
        cursor = client.cursor()
        if many:
            cursor.executemany(db_query, params)
        else:
            cursor.execute(db_query, params)
        client.commit()
        cursor.close()
        # 短连接，用完就断开
        client.close()

    @classmethod
    def update_one(cls, db_config, db_query, params=None):
        """
        执行更新操作
        :param db_config: 连接参数
        :param db_query: 更新语句
        :param params: 其他参数
        :return: 无
        """
        if params is None:
            params = tuple()
        cls.__execute(db_config, db_query, params)

    @classmethod
    def insert_one(cls, db_config, db_query, params=None):
        """
        执行插入操作
        :param db_config: 连接参数
        :param db_query: 插入语句
        :param params: 其他参数
        :return: 无
        """
        if params is None:
            params = tuple()
        cls.__execute(db_config, db_query, params)

    @classmethod
    def update_many(cls, db_config, db_query, params):
        """
        一次执行多个更新操作
        :param db_config: 连接参数
        :param db_query: 更新语句
        :param params: 其他参数
        :return: 无
        """
        cls.__execute(db_config, db_query, params, True)

    @classmethod
    def insert_many(cls, db_config, db_query, params):
        """
        一次执行多个插入操作
        :param db_config: 连接参数
        :param db_query: 插入语句
        :param params: 其他参数
        :return: 无
        """
        cls.__execute(db_config, db_query, params, True)

    @classmethod
    def __fetch(cls, db_config, db_query, params, many=False, size=None):
        """
        执行查询操作
        :param db_config: 连接参数
        :param db_query: 查询语句
        :param params: 查询参数
        :param size: 个数
        :return: 查询结果
        """
        client = cls.__init_client(db_config)
        cursor = client.cursor()
        cursor.execute(db_query, params)
        if many:
            if size is not None:
                result = cursor.fetchmany(size)
            else:
                result = cursor.fetchall()
        else:
            result = cursor.fetchone()
        cursor.close()
        # 短连接，用完就断开
        client.close()
        return result

    @classmethod
    def find_one(cls, db_config, db_query, params=None):
        """
        查询满足条件的一条数据
        :param db_config: 连接参数
        :param db_query: 查询语句
        :param params: 查询参数
        :return: 查询结果
        """
        if params is None:
            params = tuple()
        return cls.__fetch(db_config, db_query, params)

    @classmethod
    def find_many(cls, db_config, db_query, size=None, params=None):
        """
        查询所有满足条件的数据
        :param db_config: 连接参数
        :param db_query: 查询语句
        :param size: 个数
            为None表示获取全部数据
        :param params: 查询参数
        :return: 查询结果
        """
        if params is None:
            params = tuple()
        return cls.__fetch(db_config, db_query, params, True, size)
