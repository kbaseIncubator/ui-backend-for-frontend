import unittest
from BFF import (app, get_userProfile, get_narrative_list_route)
import json
import os

def test_client():
    app.config['TESTING'] = True
    return app.test_client()

class WidgetTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join( THIS_FOLDER, 'testprofile.json')
        with open(json_path) as json_file:
            cls.data = json.load(json_file)

    def test_userProfile(self):

        self.assertEqual(get_userProfile('soratest'), json.dumps(self.data))

    def test_fetchUserProfiles(self):
        client = test_client()
        response = client.post('/fetchUserProfiles', json=dict(
            users=['soratest', 'not-a-real-user'],
        ), follow_redirects=True)
        assert response.status_code == 200

    def test_teapot(self):
        client = test_client()
        response = client.get('/brew_coffee')
        assert response.status_code == 418


if __name__ == '__main__':
    unittest.main()
