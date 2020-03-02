# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy import Field
from scrapy.loader import ItemLoader

from scrapy.loader.processors import Identity, Compose, MapCompose, TakeFirst, Join

from dateutil.parser import parse as dateutil_parse
from w3lib.html import remove_tags


class BookItem(scrapy.Item):
    # Scalars
    url = Field()

    title = Field(input_processor=MapCompose(str.strip))
    author = Field(input_processor=MapCompose(str.strip))

    num_ratings = Field(input_processor=MapCompose(str.strip, int))
    num_reviews = Field(input_processor=MapCompose(str.strip, int))
    avg_rating = Field(input_processor=MapCompose(str.strip, float))
    isbn = Field()
    id = Field()
    author_url = Field()
    image_url = Field()
    similar_books = Field()
    pass




class BookLoader(ItemLoader):
    default_output_processor = TakeFirst()


class AuthorItem(scrapy.Item):
    # Scalars
    url = Field()

    name = Field()



    avg_rating = Field(serializer=float)
    num_ratings = Field(serializer=int)
    num_reviews = Field(serializer=int)

    id = Field()
    image_url = Field()
    # Lists
    related_authors = Field()
    books = Field()
    pass


class AuthorLoader(ItemLoader):
    default_output_processor = TakeFirst()
