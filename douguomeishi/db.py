#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/16 下午 05:28
# @Author  : gao
# @File    : db.py
import pymongo

from pymongo.collection import Collection


class Connect_Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db_data = self.client['dou_guo_mei_shi']

    def insert_item(self, item):
        db_collection = Collection(self.db_data, 'mei_shi')
        db_collection.insert_one(item)


mongo_info = Connect_Mongo()
