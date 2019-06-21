import unittest
from BFF import (get_userProfile, get_narrative_list_route)
import json
import os



class WidgetTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join( THIS_FOLDER, 'myprofile.json')
        with open(json_path) as json_file:
            cls.data = json.load(json_file)

    def test_userProfile(self): 
       
        self.assertEqual(get_userProfile('amarukawa'), json.dumps(self.data))


if __name__ == '__main__':
    unittest.main()
