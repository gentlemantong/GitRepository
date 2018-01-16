# -*- coding:utf-8 -*-
"""
@author: tongxiao
@email: tongxiao@yeah.net
@created_time: 2018-01-04 13:06
"""
import logging

from elasticsearch import Elasticsearch
from elasticsearch import helpers

from slow_sql_monitor.config import ES_TIMEOUT

logger = logging.getLogger(__name__)


class ElasticClient(object):
    """
    常用的ES相关方法
    """

    @staticmethod
    def create_index(hosts, index, ignore=400):
        """
        创建一个index
        :param hosts: 节点连接参数列表，eg: [{'host': 'host1', 'port': 'port1'}, {'host': 'host2', 'port': 'port2'}]
        :param index: 索引
        :param ignore: ignore参数，400表示如果已经存在这个index就忽略
        :return: 执行结果
        """
        es = Elasticsearch(hosts, timeout=ES_TIMEOUT)
        return es.indices.create(index=index, ignore=ignore)

    @staticmethod
    def delete_index(hosts, index, ignore=400):
        """
        删除一个index(慎重使用)
        :param hosts: 节点连接参数列表，eg: [{'host': 'host1', 'port': 'port1'}, {'host': 'host2', 'port': 'port2'}]
        :param index: 索引
        :param ignore: ignore参数，400表示如果已经存在这个index就忽略
        :return: 执行结果
        """
        es = Elasticsearch(hosts, timeout=ES_TIMEOUT)
        return es.indices.delete(index, ignore=ignore)

    @staticmethod
    def insert_one(hosts, index, doc_type, body, doc_id=None, params=None):
        """
        在特定索引中添加或更新类型化的JSON文档，使其可搜索
        :param hosts: 节点连接参数列表
        :param index: 索引
        :param doc_type: 文档类型
        :param body: 文档内容
        :param doc_id: 文档ID，不指定的话会自动生成
        :param params: 其他参数
        :return: 执行结果
        """
        es = Elasticsearch(hosts, timeout=ES_TIMEOUT)
        return es.index(index, doc_type, body, doc_id, params)

    @staticmethod
    def insert_many(hosts, index, actions):
        """
        在单个API调用中执行许多索引/删除操作
        :param hosts: 节点连接参数列表
        :param index: 索引
        :param actions: 需要存储的内容列表
        :return: 执行结果
        """
        es = Elasticsearch(hosts, timeout=ES_TIMEOUT)
        return helpers.bulk(es, actions, index=index)

    @staticmethod
    def find_one_by_id(hosts, index, doc_type, doc_id, params=None):
        """
        获取满足条件的一条数据(需要指定ID)
        :param hosts: 节点连接参数列表
        :param index: 索引
        :param doc_type: 文档类型
        :param doc_id: 文档ID
        :param params: 其他参数
        :return: 查询结果，字典
        """
        es = Elasticsearch(hosts, timeout=ES_TIMEOUT)
        return es.get(index, doc_type, doc_id, params)

    @staticmethod
    def find_many(hosts, index=None, doc_type=None, body=None):
        """
        执行搜索查询并返回与查询匹配的搜索命中
        :param hosts: 节点连接参数/参数列表
        :param index: 索引/索引列表
        :param doc_type: 类型/类型列表
        :param body: 查询语句
        :param params: 其他参数
        :return: 查询结果，字典类型
        """
        es = Elasticsearch(hosts, timeout=ES_TIMEOUT)
        return es.search(index, doc_type, body)

    @staticmethod
    def delete_one_by_id(hosts, index, doc_type, doc_id, params=None):
        """
        根据文档ID删除特定索引下的一个文档
        :param hosts: 节点连接参数列表
        :param index: 索引
        :param doc_type: 文档类型
        :param doc_id: 文档ID
        :param params: 其他参数
        :return: 执行结果
        """
        es = Elasticsearch(hosts, timeout=ES_TIMEOUT)
        return es.delete(index, doc_type, doc_id, params)

    @staticmethod
    def delete_many(hosts, index, body, doc_type, params=None):
        """
        删除匹配查询的所有文档
        :param hosts: 节点连接参数列表
        :param index: 索引
        :param body: 删除条件
        :param doc_type: 文档类型
        :param params: 其他参数
        :return: 执行结果
        """
        es = Elasticsearch(hosts, timeout=ES_TIMEOUT)
        return es.delete_by_query(index, body, doc_type, params)

    @staticmethod
    def count(hosts, index=None, doc_type=None, body=None, params=None):
        """
        执行查询并获取该查询的匹配数
        :param hosts: 节点连接参数列表
        :param index: 索引
        :param doc_type: 文档类型
        :param body: 查询语句
        :param params: 其他参数
        :return: 执行结果
        """
        es = Elasticsearch(hosts, timeout=ES_TIMEOUT)
        return es.count(index, doc_type, body, params)

    @staticmethod
    def exists(hosts, index, doc_type, doc_id, params=None):
        """
        返回一个布尔值，指示是否给定的文档存在于Elastic search
        :param hosts: 节点连接参数列表
        :param index: 索引
        :param doc_type: 文档类型
        :param doc_id: 文档id
        :param params: 其他参数
        :return: 执行结果
        """
        es = Elasticsearch(hosts, timeout=ES_TIMEOUT)
        return es.exists(index, doc_type, doc_id, params)
