from copy import deepcopy
import unittest
import json

import api

BASE_URL = 'http://127.0.0.1:5000/'
BAD_ITEM_URL = '{}/5'.format(BASE_URL)
GOOD_ITEM_URL = '{}/3'.format(BASE_URL)
class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        self.api = api.app.test_client()
        self.api.testing = True

    def test_get_all(self):
        response = self.api.get("http://127.0.0.1:5000/query/most-similar-book")

        self.assertEqual(response.status_code, 200)

    def test_get_wrong(self):
        response = self.api.get("http://127.0.0.1:5000/query/most-similar-books")

        self.assertEqual(response.status_code, 404)


    def test_find_wrongbook(self):
        response = self.api.get("http://127.0.0.1:5000/authors/title=fuckyou")

        self.assertEqual(response.status_code, 400)

    def test_find_wrongtitle(self):
        response = self.api.get("http://127.0.0.1:5000/authors/titless=Feather")

        self.assertEqual(response.status_code, 400)

    def test_findBook_success(self):
        response = self.api.get("http://127.0.0.1:5000/books/title=Feathers")

        self.assertEqual(response.status_code, 200)

    def test_findauthor_success(self):
        response = self.api.get("http://127.0.0.1:5000/authors/name=Joyce Sidman")

        self.assertEqual(response.status_code, 200)

    def test_findauthor_falsename(self):
        response = self.api.get("http://127.0.0.1:5000/authors/name=Joyce Sidmwwan")

        self.assertEqual(response.status_code, 400)


    def test_findauthor_false(self):
        response = self.api.get("http://127.0.0.1:5000/authors/title=Joyce Sidman")

        self.assertEqual(response.status_code, 400)
    # def test_get_one(self):
    #     response = self.api.get(BASE_URL)
    #     data = json.loads(response.get_data())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['items'][0]['name'], 'laptop')
    #
    # def test_item_not_exist(self):
    #     response = self.api.get(BAD_ITEM_URL)
    #     self.assertEqual(response.status_code, 404)
    #
    # def test_post(self):
    #     # missing value field = bad
    #     item = {"name": "some_item"}
    #     response = self.api.post(BASE_URL,
    #                              data=json.dumps(item),
    #                              content_type='apilication/json')
    #     self.assertEqual(response.status_code, 400)
    #     # value field cannot take str
    #     item = {"name": "screen", "value": 'string'}
    #     response = self.api.post(BASE_URL,
    #                              data=json.dumps(item),
    #                              content_type='apilication/json')
    #     self.assertEqual(response.status_code, 400)
    #     # valid: both required fields, value takes int
    #     item = {"name": "screen", "value": 200}
    #     response = self.api.post(BASE_URL,
    #                              data=json.dumps(item),
    #                              content_type='apilication/json')
    #     self.assertEqual(response.status_code, 201)
    #     data = json.loads(response.get_data())
    #     self.assertEqual(data['item']['id'], 4)
    #     self.assertEqual(data['item']['name'], 'screen')
    #     # cannot add item with same name again
    #     item = {"name": "screen", "value": 200}
    #     response = self.api.post(BASE_URL,
    #                              data=json.dumps(item),
    #                              content_type='apilication/json')
    #     self.assertEqual(response.status_code, 400)
    #
    # def test_update(self):
    #     item = {"value": 30}
    #     response = self.api.put(GOOD_ITEM_URL,
    #                             data=json.dumps(item),
    #                             content_type='apilication/json')
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.get_data())
    #     self.assertEqual(data['item']['value'], 30)
    #     # proof need for deepcopy in setUp: update api.items should not affect self.backup_items
    #     # this fails when you use shallow copy
    #     self.assertEqual(self.backup_items[2]['value'], 20)  # org value
    #
    # def test_update_error(self):
    #     # cannot edit non-existing item
    #     item = {"value": 30}
    #     response = self.api.put(BAD_ITEM_URL,
    #                             data=json.dumps(item),
    #                             content_type='apilication/json')
    #     self.assertEqual(response.status_code, 404)
    #     # value field cannot take str
    #     item = {"value": 'string'}
    #     response = self.api.put(GOOD_ITEM_URL,
    #                             data=json.dumps(item),
    #                             content_type='apilication/json')
    #     self.assertEqual(response.status_code, 400)
    #
    # def test_delete(self):
    #     response = self.api.delete(GOOD_ITEM_URL)
    #     self.assertEqual(response.status_code, 204)
    #     response = self.api.delete(BAD_ITEM_URL)
    #     self.assertEqual(response.status_code, 404)
    #
    # def tearDown(self):
    #     # reset api.items to initial state
    #     api.items = self.backup_items


if __name__ == "__main__":
    unittest.main()