# Start of Backend For Frontend

Backend for frontend was developed to shift API calls and data wrangling within browser script to server script to aim faster loading, quicker data structure modification to fit UI development needs, and to provide reusable data structures.

## Installation

- It is best that you [create a virtual environment][creating-venv].
- Clone the repo on your local machine and install dependencies.

```bash
$ pip install -r requirements.txt
```

- You may then run an instance of the server with the following command:

```bash
$ FLASK_APP=BFF:app FLASK_ENV=development python -m flask run --debugger --port $PORT
```

- The unit tests may then be run with

```bash
python -m unittest discover -v Test
```

[creating-venv]: https://docs.python.org/3/library/venv.html#creating-virtual-environments

### Locally build Docker countainer and run image

Go to the project root folder and run

`$ sh scripts/start_docker_server.sh`


### Document

@app.route('/spec') returns quick summary of paths/discriptions/method/versions of services that are used for the route.

## 🍔 SO what's in it? 🍱

Each route shall have following information:

- @app.route
- Synopsis
- Reference docs
  - link to github spec or readme
- API calls
  - method and service
- Data wrangling
  - https://en.wikipedia.org/wiki/Data_wrangling
- Response
  - shape of response

## app.route('/fetchUserProfile/< userID >')

### Synopsis:
With userID of the profile, it returns the full information (which is documented as "UnspecifiedObject" in [UserProfile.spec][UserProfile.spec]).

### Reference docs:

[UserProfile.spec][UserProfile.spec]

### API calls:

1. POST request to user profile rpc

### Parameters:

- user id (string) in path

### Data wrangling:

- user profile service does not return keys that does not contain matching value. Add them on so that browser script does not require to check if it is 'undefined".

### Response:

<details>
<summary>Sample JSON response</summary>

```json
{
  "version": "1.1",
  "result": [
    [
      {
        "user": {
          "username": "maruthecat",
          "realname": "Maru The Cat"
        },
        "profile": {
          "metadata":
            {
              "createdBy": "userprofile_ui_service",
              "created": "2018-12-11T22:16:45.905Z"
            },
          "preferences": {},
          "userdata":
            {
              "organization": "Lawrence Berkeley National Laboratory (LBNL)",
              "department": "Dog wrangling",
              "city": "Berkeley",
              "state": "California",
              "postalCode": "94720",
              "country": "United States",
              "affiliations": [
                {
                  "title": "Cat herder",
                  "organization": "Western Mountain Sports",
                  "started": "1969",
                  "ended": "Present"
                },
                {
                  "title": "Cat nip tester",
                  "organization": "Chillmix",
                  "started": "1969","ended": "1973"
                }
              ],
              "researchStatement": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec non eleifend tortor. Curabitur finibus pulvinar orci, at vulputate leo. Phasellus pretium lectus non magna tempus, sed vehicula justo porttitor.",
              "jobTitle": "Other",
              "jobTitleOther": "Front end dev",
              "researchInterests": [
                "Genome Annotation","Genome Assembly","Microbial Communities","Comparative Genomics","Expression","Metabolic Modeling","Read Processing","Sequence Analysis","Utilities","Other"
              ],
              "fundingSource": "DOE National Nuclear Security Administration (NNSA)",
              "gravatarDefault": "mm"},
              "synced": {"gravatarHash": "4210d8e14db97e647b8cedc9fa3c4119"},
              "plugins": {
          "data-search": {
            "settings": {
              "history": {
                "search": {
                  "history": [],
                    "time": {
                      "$numberLong": "1546649250079"
                    }
                  }
                }
              }
            }
          }
        }
      }
    ]
  ]
}
```
</details>

## @app.route('/fetchUserProfiles')

### Synopsis:
When this route recieves a POST request with a JSON body from a JS object like
```js
{ users: [...userIDs] }
```
this route will return an array of the profiles for each user, and `null` if a
userID is not found.

### Reference docs:

[UserProfile.spec][UserProfile.spec]

[UserProfile.spec]: https://github.com/kbase/user_profile/blob/master/UserProfile.spec

### API calls:

1. This route makes a POST request to user profile rpc

### Parameters:

- An `application/json` body in a POST request with an object like
```js
{ users: [...userIDs] }
```

### Data wrangling:

- There is no data wrangling for this route.

### Response:

<details>
<summary>Sample JSON response</summary>

```json
{
  "version": "1.1",
  "result": [
    [
      {
        "user": {
          "username": "soratest",
          "realname": "Sora Bear"
        },
        "profile": {
          "metadata": {
            "createdBy": "userprofile_ui_service",
            "created": "2019-06-24T21:32:45.552Z"
          },
          "preferences": {},
          "userdata": {
            "organization": "Lawrence Berkeley National Laboratory (LBNL)",
            "department": "Kbase",
            "city": "San Francisco",
            "state": "California",
            "postalCode": "94122",
            "country": "United States",
            "fundingSource": "Other",
            "avatarOption": "gravatar",
            "gravatarDefault": "monsterid",
            "researchStatement": "This profile is made for testing. ",
            "jobTitle": "Other",
            "jobTitleOther": "Dev",
            "researchInterests": [
              "Genome Annotation",
              "Genome Assembly",
              "Microbial Communities",
              "Comparative Genomics",
              "Expression"
            ]
          },
          "synced": {
            "gravatarHash": "7c4edb6cbe9e46cdf4f57314caecf69f"
          }
        }
      },
      null
    ]
  ]
}
```
</details>

## @app.route('/narrative_list/< param_type >' ) - calling this twice from frontend

### Synopsis:

With one of following parameters: mine, shared, and public, it returns narratives with narrative detail.

### Reference Docs:

-   https://kbase.us/services/ws/docs/Workspace.html#typedefWorkspace.ObjectIdentity
-   https://github.com/kbaseapps/NarrativeService/blob/master/NarrativeService.spec

### API calls:

1. POST request to service wizard to get dynamic service URL
2. POST request to narrative service to get list of narratives
3. POST request to workspace service to get users have access to each narratives.
4. REPEAT step 1 - step 3 for each users (Public & Shared/Mine & Shared)

### Parameters:

- search parameter(string) in path
- token (string) in headers

```
headers: {
  Authorization: KBase session cookie in string
}
```

### Data wrangling:

-   Filter narratives( work space ) with "narrative_nice_name" and return the list
-   Each narrative last saved date is converted to the number of milliseconds since January 1, 1970, 00:00:00 UTC.

### Response:

Array of narrative data object

<details>
<summary>Sample JSON response</summary>

```json
[
  {
    "wsID": 39031,
    "permission": "a",
    "name": "Luna pughuahua sampling",
    "last_saved": 1559254557000,
    "users": {},
    "narrative_detail":
      {
        "creator": "maruthecat",
        "data_dependencies": "[]",
        "jupyter.markdown": "1",
        "is_temporary": "false",
        "job_info": "{\"queue_time\": 0, \"running\": 0, \"completed\": 0, \"run_time\": 0, \"error\": 0}",
        "format": "ipynb",
        "name": "Luna pughuahua sampling",
        "description": "",
        "method.MEGAHIT/run_megahit/cc91ddfe376f907aa56cfb3dd1b1b21cae8885a6": "1",
        "type": "KBaseNarrative.Narrative",
        "ws_name": "maruthecat:narrative_1547057225124"
      }
    },
```
</details>

## @app.route('/org_list/< profileID >')

### Synopsis:
Returns list of the orgs that both logged in user and profile user are in.

### API calls:

1.  GET request to group service to fetch organization that user is associated
2.  GET request to group service to to get detailed organization information. Mainly to get list of admin, owner, and members
3.  REPEAT step 2 as many times as the number of orgs step 1 returned.

### Parameters:

- user id (string) in path
- token (string) in headers

```typescript
headers: {
  Authorization: "KBase session cookie in string"
}
```

### Data wrangling

-   filter organization list that logged in user is associated to the ones the profile user is also associated with.

### Response:

Array of org name and id

```typescript
Org {
      name:  string;
      id:  string;
}
```
