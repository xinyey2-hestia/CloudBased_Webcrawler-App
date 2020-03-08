from flask_testing import TestCase
from flask import Flask, jsonify


class MyTest(TestCase):
    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

@app.route("/ajax/")
def some_json():
    return jsonify(success=True)

class TestViews(TestCase):
    def test_some_json(self):
        response = self.client.get("/ajax/")
        self.assertEquals(response.json, dict(success=True))