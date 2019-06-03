import os
import requests
import json
from flask import Flask
import datetime

app = Flask(__name__)

public_narrative = []
shared_narrative = []


# @app.route('/narrative_list/<param_type>/<token>')
# Get list of narratives with auth
# Return an array of narrativeData objects
    # {wsID: string; 
    # name: string; 
    # last_saved: string;
    # users: Array<string>; -- users that native owner shared the narrative with
    # narrative_detail: object;}
@app.route('/narrative_list/<param_type>/<token>')
# get dynamic service URL first
def get_narrative_list_route(param_type, token):
    #print(param_type)
    #print('in get narrative url list https://ci.kbase.us/services/service_wizard')
    narrative_service_url_payload = {
        'id': 0,
        'method': 'ServiceWizard.get_service_status',
        'version': '1.1',
        'params': [
                {
                    'module_name': 'NarrativeService',
                    'version': None
                }
            ],
    }
    
    headers = {'Authorization' : token}
    response = requests.post('https://ci.kbase.us/services/service_wizard', data=json.dumps(narrative_service_url_payload), headers=headers)

    try:
        resp_json = response.json()
        url = resp_json['result'][0]['url']

    except Exception:
        print('Error during fetching dynamic service (NarrativeSericve module) url', response)
    # fetch narrative list with the url
    narrative_list = get_narrative_list(url, param_type, token)
    return narrative_list

# Fetch narrative list
def get_narrative_list(narrative_service_url, param_type, token):
    # print('in get narrative list https://ci.kbase.us/services/service_wizard')
    narrative_list_payload = {
        'id': 0,
        'method': 'NarrativeService.list_narratives',
        'version': '1.1',
        'params': [{'type': param_type}],
    }
    headers = {'Authorization' : token}
    res = requests.post(narrative_service_url, data=json.dumps(narrative_list_payload), headers=headers)

    try:
        res_json = res.json()
    except Exception:
        print('Error during fetching narrative list', res)
    # Filter narratives( work space ) with "narrative_nice_name" and return the list
    # print(res_json['result'][0]['narratives'])
    narrative_list = []
    WorkspaceIdentityList = []
    for ws in res_json['result'][0]['narratives']:
        if 'narrative_nice_name' in ws['ws'][8]:
            epoch = datetime.datetime.utcfromtimestamp(0)
            converted_date = datetime.datetime.strptime(ws['ws'][3], '%Y-%m-%dT%H:%M:%S+%f')
            # print((converted_date - epoch).total_seconds()* 1000)
            last_saved = (converted_date - epoch).total_seconds()* 1000
            # last_saved = str(converted_date.month) + '/' + str(converted_date.day) + '/' + str(converted_date.year) + ' @ ' + str(converted_date.hour) + ":" + str(converted_date.minute) 
            narrative_list.append({'wsID': ws['ws'][0], 'permission': ws['ws'][5], 'name': ws['ws'][8]['narrative_nice_name'], 'last_saved': last_saved, 'users': {},'narrative_detail': ws['nar'][10]})
            WorkspaceIdentityList.append({'id': ws['ws'][0]})
            # print ('list', WorkspaceIdentityList)
        
    #get_narrative_users(WorkspaceIdentityList, token)
    #return json.dumps(res_json['result'][0]['narratives'])
    return json.dumps(narrative_list)
    

# Fetch users for each narrative that owner shared the narrative with.
# Param: array of user dictionary 
def get_narrative_users(WorkspaceIdentityList, token):

    narrative_users_payload = {
        'version': '1.1',
        'method': 'Workspace.get_permissions_mass',
        'params': [{'workspaces': WorkspaceIdentityList}],
    }
    headers = {'Authorization' : token}
    res_permission = requests.post('https://ci.kbase.us/services/ws', data=json.dumps(narrative_users_payload), headers=headers)
    try:
        res_permission_json = res_permission.json()
        print('res_list_json', res_permission_json['result'][0]['perms'])
    except Exception:
        print('Error during fetching narrative list',  res_permission)
        

# Fetch user profile
@app.route('/fetchUserProfile/<userID>')
def get_userPofile(userID):
    userProfile_payload = {
        'id': 0,
        'method': 'UserProfile.get_user_profile',
        'version': '1.1',
        'params': [[userID]]
    }

    response = requests.post(
        'https://ci.kbase.us/services/user_profile/rpc', data=json.dumps(userProfile_payload))
    try:
        response_json = response.json()
        # print('profile_respons', response_json['result'][0][0]['profile']['userdata']['avatarOption'])
        
        # If there is no end year entered, add ended - Present
        for index in response_json['result'][0][0]['profile']['userdata']['affiliations']:
            if 'ended' not in index:
                index['ended'] = "Present"
            else:
                pass

    except Exception:
        print('Error during fetching user profile', response)

    return json.dumps(response_json)


@app.after_request
def after_request(resp):
    # Enable CORS
    resp.headers['Access-Control-Allow-Origin'] = '*'
    env_allowed_headers = os.environ.get(
        'HTTP_ACCESS_CONTROL_REQUEST_HEADERS', 'Authorization, Content-Type')
    resp.headers['Access-Control-Allow-Headers'] = env_allowed_headers
    # Set JSON content type and response length
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Content-Length'] = resp.calculate_content_length()
    return resp
