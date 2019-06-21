import unittest
from BFF import (get_userProfile, get_narrative_list_route)
import json
import os

# THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# json_file = os.path.join( THIS_FOLDER, 'myprofile.json')
# with open('json_file') as json_file:
#     data = json.load(json_file)


class WidgetTestCase(unittest.TestCase):


    def test_userProfile(self): 
        data = {
            "user": {
                "username": "amarukawa",
                "realname": "Akiyo Marukawa"
            },
            "profile": {
                "metadata": {
                    "createdBy": "userprofile_ui_service",
                    "created": "2018-11-14T17:31:03.569Z"
                },
                "preferences": {},
                "userdata": {
                    "organization": "Lawrence Berkeley National Laboratory (LBNL)",
                    "department": "EB-Environ Genomics & Systems Bio",
                    "city": "Berkeley",
                            "state": "California",
                            "postalCode": "94720",
                            "country": "United States",
                            "fundingSource": "Other",
                            "avatarOption": "gravatar",
                            "gravatarDefault": "monsterid",
                            "researchStatement": "Front End Dev Software Engineer",
                            "researchInterests": ["Other"],
                            "affiliations": [
                                    {
                                            "title": "Engineer",
                                            "organization": "Foo",
                                            "started": "2014",
                                            "ended": "2015"
                                    }
                            ],
                    "jobTitle": "Other",
                    "jobTitleOther": "Front End Dev"
                },
                "synced": {
                    "gravatarHash": "4210d8e14db97e647b8cedc9fa3c4119"
                },
                "plugins": {
                    "data-search": {
                        "settings": {
                            "history": {
                                "search": {
                                    "history": [
                                        "24019",
                                        "g",
                                        "phenotypes",
                                        "Acaryochloris"
                                    ],
                                    "time": 1554240106923
                                }
                            }
                        }
                    },
                    "jgi-search": {
                        "settings": {
                            "history": {
                                "search": {
                                    "history": [],
                                    "time": 1549389043906
                                }
                            },
                            "jgiDataTerms": {
                                "agreed": True,
                                "time": 1549389047905
                            }
                        }
                    }
                }
            }
        }
        self.assertEqual(get_userProfile('amarukawa'), json.dumps(data))


if __name__ == '__main__':
    unittest.main()
