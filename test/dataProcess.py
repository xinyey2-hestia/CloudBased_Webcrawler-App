import unittest
import helper
import os

class MyTestCase(unittest.TestCase):

    def test_something(self):
        path = os.path.dirname(__file__)
        dir_data = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), r"data.json")
        aj, bj = helper.jsonParse(dir_data)
        assert(aj[0]['title']=="Feathers")

    def test_ranking(self):
        path = os.path.dirname(__file__)
        dir_data = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), r"data.json")
        aj, bj = helper.jsonParse(dir_data)
        labels = []
        values = []
        count = 0
        for i in bj:
            labels.append(i['name'])
            values.append(float(i['rating']))

        labels = [x for y, x in sorted(zip(values, labels), reverse=True)]
        values.sort(reverse=True)
        assert (values[0]>values[4])

    def test_ranking2(self):
        path = os.path.dirname(__file__)
        dir_data = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), r"data.json")
        aj, bj = helper.jsonParse(dir_data)
        labels = []
        values = []
        count = 0
        for i in aj:
            labels.append(i['title'])
            values.append(float(i['rating']))

        labels = [x for y, x in sorted(zip(values, labels), reverse=True)]
        values.sort(reverse=True)
        assert (values[0]>values[4])


if __name__ == '__main__':
    unittest.main()
