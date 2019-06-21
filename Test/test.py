import unittest
from BFF import (get_userProfile, get_narrative_list_route)
import json


class WidgetTestCase(unittest.TestCase):
    
    def test_userProfile(self):
        with open('myprofile.json') as json_file:  
            data = json.load(json_file)

        self.assertEqual(get_userProfile('amarukawa'), data)

if __name__ == '__main__':
    unittest.main()