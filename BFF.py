# TODO:AKIYO Make this to strong typed
# TODO:AKIYO Dvelop a test to run when the backend changes

"""
Backend For Frontend - User profile view

"""
import os
import requests
import json
from flask import Flask, jsonify, request
from flask_swagger import swagger
import datetime
import exceptions
app = Flask(__name__)

conf = dict()
# conf['KBASE_ENDPOINT'] = 'https://kbase.us/services'
conf['KBASE_ENDPOINT'] = os.environ.get(
    'KBASE_ENDPOINT', 'https://kbase.us/services')
# assert os.environ.get('KBASE_ENDPOINT', '').strip(
# ), "KBASE_ENDPOINT env var is required."

# spec of the BFF APIs
@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = '1.0'
    swag['info']['title'] = 'KBase UI backend for frontend'
    swag['info']['description'] = 'Initial commit June 2019'
    return jsonify(swag)

# register error handlers
@app.errorhandler(500)
def network_error(error):
    return 'Internal Server Error, 500', 500


@app.errorhandler(exceptions.AuthError)
def auth_error(error):
    return 'Authentication Error, 401', 401


@app.errorhandler(400)
def bad_request(error):
    return 'Bad request, 400', 400


@app.errorhandler(404)
@app.errorhandler(exceptions.NotFound)
def not_found(error):
    return 'Not found, 404', 404


@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({
        'error': str(error),
        'error_class': str(error.__class__)
    }), 500


@app.route("/brew_coffee")
def imateapot():
    return "I'm a teapot", 418

# Check which error


def which_error(response):
    if response.status_code == 401:
        raise exceptions.AuthError()
    elif response.status_code == 500:
        raise Exception(response.text)
    elif response.status_code == 404:
        # Not in the group
        raise exceptions.NotFound()


@app.route('/org_list/<profileID>')
def get_org_list(profileID):
    """
    Returns list of orgs that both profile and the logged in users 
    are associated with. 
    ---
    responses:
        '401':
            description: Authorized. Invalid token or token missing.
        '200':
            description: https://github.com/kbaseIncubator/ui-backend-for-frontend#response-2
    tags: 
        - orgs
        - Groups-service-version-0.1.6
    summary: https://github.com/kbaseIncubator/ui-backend-for-frontend#approuteorg_list-profileid--token- 
    externalDocs: https://github.com/kbase/groups

    """
    try:
        # check if auth token is there
        auth_token = request.headers['Authorization']

    except Exception:
        raise exceptions.AuthError

    headers = {'Authorization': auth_token}
    groupUrl = conf['KBASE_ENDPOINT'] + '/groups/member/'
    response = requests.get(groupUrl, headers=headers)
    if not response.ok:
        which_error(response)
    else:
        org_list = response.json()

    # get org info for each org, and filter orgs that profile is
    # also associated with.
    all_orgs = list(
        map(lambda x: get_group_info(x['id'], auth_token), org_list))
    filtered_orgs = list(
        filter(lambda y: filterorgbyprofileuser(y, profileID), all_orgs))

    return json.dumps(filtered_orgs)


def get_group_info(org_id, token):
    """ Get group info with the auth token and org id. """

    groupUrl = conf['KBASE_ENDPOINT'] + '/groups/group/' + org_id
    headers = {'Authorization': token}
    response = requests.get(groupUrl, headers=headers)
    if not response.ok:
        which_error(response)

    return response.json()


def filterorgbyprofileuser(org_info, profileID):
    """ Check if the profile ID is in member/admin/owner of the org.
        retruns True/False. """
    org_members = list(filter(lambda x: x['name'] == profileID, [
                       org_info['owner']] +
        org_info['admins'] +
        org_info['members']))
    if len(org_members) > 0:
        return True
    else:
        return False


@app.route('/narrative_list/<param_type>', methods=['GET'])
def get_narrative_list_route(param_type):
    """
    Returns list of narratives from one of following parameters: mine, public, 
    shared.
    Get dynamic serivice url first, then fetch narrative list.
    Map list with creators.
    ---
    responses:
          200:
            description: https://github.com/kbaseIncubator/ui-backend-for-frontend#response-1
    tags:
        - narrative
        - service_wizard-module-version-0.4.1  
        - NarrativeService-module-version-0.2.3
        - workspace-service-version-0.8.2
    summary: fetch user profile from userID
    externalDocs: https://kbase.us/services/ws/docs/Workspace.html
    description: https://github.com/kbaseIncubator/ui-backend-for-frontend#approutenarrative_list-param_type--token-----calling-this-twice-from-frontend 
    """
    try:
        # check if auth token is there
        auth_token = request.headers['Authorization']

    except Exception:
        raise exceptions.AuthError
    # Get service wizerd url first.
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

    headers = {'Authorization': auth_token}
    service_wizard_url = conf['KBASE_ENDPOINT'] + '/service_wizard'
    response = requests.post(service_wizard_url, data=json.dumps(
        narrative_service_url_payload), headers=headers)

    if not response.ok:
        which_error(response)

    else:
        resp_json = response.json()
        url = resp_json['result'][0]['url']

    # fetch narrative list with the service wizerd url
    narrative_list = get_narrative_list(url, param_type, auth_token)
    return json.dumps(narrative_list)


def get_narrative_list(narrative_service_url, param_type, auth_token):
    """ Fetch narrative list """
    narrative_list_payload = {
        'id': 0,
        'method': 'NarrativeService.list_narratives',
        'version': '1.1',
        'params': [{'type': param_type}],
    }
    headers = {'Authorization': auth_token}
    response = requests.post(narrative_service_url, data=json.dumps(
        narrative_list_payload), headers=headers)
    if not response.ok:
        which_error(response)
    else:
        res_json = response.json()

    # Filter narratives( work space ) with "narrative_nice_name" and return
    # the list
    narrative_list = []
    WorkspaceIdentityList = []
    for ws in res_json['result'][0]['narratives']:
        if 'narrative_nice_name' in ws['ws'][8]:
            epoch = datetime.datetime.utcfromtimestamp(0)
            converted_date = datetime.datetime.strptime(
                ws['ws'][3], '%Y-%m-%dT%H:%M:%S+%f')
            last_saved = (converted_date - epoch).total_seconds() * 1000
            narrative_list.append({
                'wsID': ws['ws'][0],
                'permission': ws['ws'][5],
                'name': ws['ws'][8]['narrative_nice_name'],
                'owner': ws['ws'][2],
                'last_saved': last_saved,
                'users': {},
                'narrative_detail': ws['nar'][10]
            })
            WorkspaceIdentityList.append({'id': ws['ws'][0]})

    # use get_narrative_users function to get users that narratives are
    #  shared with.
    # get_narrative_users(WorkspaceIdentityList, narrative_list, auth_token)
    return narrative_list


def get_narrative_users(WorkspaceIdentityList, narrative_list, auth_token):
    """Fetch users for each narrative that owner shared the narrative with.
    Param: array of user dictionary."""

    narrative_users_payload = {
        'version': '1.1',
        'method': 'Workspace.get_permissions_mass',
        'params': [{'workspaces': WorkspaceIdentityList}],
    }
    headers = {'Authorization': auth_token}
    ws_url = conf['KBASE_ENDPOINT'] + '/services/ws'
    response = requests.post(ws_url, data=json.dumps(
        narrative_users_payload), headers=headers)

    if not response.ok:
        which_error(response)
    else:
        response_json = response.json()

    for index, narrative in enumerate(narrative_list):
        narrative['users'] = response_json['result'][0]['perms'][index]


@app.route('/fetchUserProfile/<userID>', methods=['GET'])
def get_userProfile(userID):
    """
    Fetch user profile
    It returns user's real name and information.
    ---
    tags:
        - profile
        - userprofile-service-VERSION-0.2.1 (Released 4/1/19)
    summary: fetch user profile from userID
    externalDocs: https://github.com/kbase/user_profile/blob/master/UserProfile.spec
    responses: 
        200:
            description: https://github.com/kbaseIncubator/ui-backend-for-frontend#response
        404:
            description: User not found.  BFF returns empty profile and with 
            user name "User not found". 
    """

    userProfile_payload = {
        'id': 0,
        'method': 'UserProfile.get_user_profile',
        'version': '1.1',
        'params': [[userID]]
    }
    user_profile_rpc_url = conf['KBASE_ENDPOINT'] + '/user_profile/rpc'
    response = requests.post(
        user_profile_rpc_url, data=json.dumps(userProfile_payload))

    try:
        if not response.ok:
            raise Exception('error during fetching user profile')
        else:
            response_json = response.json()
            res = response_json['result'][0][0]

        if 'profile' not in res:
            raise exceptions.NotFound

    except Exception:
        pass

    finally:
        if res is None:
            # Send back empty profile with to avoid frontend crashing.
            res = {
                'user': {
                    'username': 'User Not found',
                    'realname': 'User Not found'
                },
                'profile': {
                    'userdata': {
                        'organization': '',
                        'department': '',
                        'city': '',
                        'state': '',
                        'postalCode': '',
                        'country': '',
                        'affiliations': [
                            {
                                        'title': '',
                                        'organization': '',
                                        'started': '',
                                        'ended': ''
                            }
                        ],
                        'avatarOption': ''
                    },
                    'synced': {
                        'gravatarHash': ''
                    }
                }
            }
            return json.dumps(res), 404

    if res['profile']['userdata'] is None:
        res['profile'] = {
            'userdata': {
                'affiliations': [{'title': '', 'organization': '',
                                  'started': '', 'ended': ''}],
                'city': '',
                'state': '',
                'postalCode': '',
                'country': '',
                'researchStatement': '',
                'fundingSource': '',
                'gravatarDefault': 'identicon',
                'avatarOption': '',
                'organization': ''
            },
            'synced': {
                'gravatarHash': ''
            }
        }

    else:
        if 'affiliations' not in res['profile']['userdata']:
            res['profile']['userdata']['affiliations'] = [
                {'title': '', 'organization': '', 'started': '', 'ended': ''}]
        else:
            # If there is no end year entered, add ended - Present
            for index in res['profile']['userdata']['affiliations']:
                if 'ended' not in index:
                    index['ended'] = "Present"

        if 'city' not in res['profile']['userdata']:
            res['profile']['userdata']['city'] = ''

        if 'state' not in res['profile']['userdata']:
            res['profile']['userdata']['state'] = ''

        if 'postalCode' not in res['profile']['userdata']:
            res['profile']['userdata']['postalCode'] = ''

        if 'country' not in res['profile']['userdata']:
            res['profile']['userdata']['country'] = ''

        if 'researchStatement' not in res['profile']['userdata']:
            res['profile']['userdata']['researchStatement'] = ''

        if 'fundingSource' not in res['profile']['userdata']:
            res['profile']['userdata']['fundingSource'] = ''

        if 'gravatarDefault' not in res['profile']['userdata']:
            res['profile']['userdata']['gravatarDefault'] = 'identicon'

        if 'avatarOption' not in res['profile']['userdata']:
            res['profile']['userdata']['avatarOption'] = ''

    return json.dumps(res)


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
