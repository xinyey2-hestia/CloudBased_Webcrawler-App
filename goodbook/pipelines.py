# -*- coding: utf-8 -*-
import pymongo
from .items import AuthorItem, BookItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class GoodbookPipeline(object):

    def __init__(self):
        client = pymongo.MongoClient("mongodb://xinyey2:7861141@cluster0-shard-00-00-2bqe9.mongodb.net:27017,cluster0-shard-00-01-2bqe9.mongodb.net:27017,cluster0-shard-00-02-2bqe9.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
        self.db = client.goodbooks_database
        self.collection = self.db.goodbooks_collection


    def process_item(self, item, spider):

        if isinstance(item,AuthorItem):
            postItem = dict(item)
            posts = self.db.authors
            posts.insert_one(postItem).inserted_id
        if isinstance(item, BookItem):
            postItem = dict(item)
            books= self.db.book
            books.insert_one(postItem).inserted_id
        return item
