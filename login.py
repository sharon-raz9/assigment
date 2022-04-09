import requests
import itertools

# I would send the connection attempts in parallel with the help of the library asyncio
_session = requests.Session()

METHODS = ['GET', 'POST']
SUCCESS_STATUS_CODES = [200, 201, 202, 204]
USE_URL_PARAMS = USE_JSON_IN_PARAMS = VERIFY_SSL = [True, False]
HEADERS = [
    None,
    {'Content-Type': 'application/json'},
    {'Content-Type', 'application/x-www-form-urlencoded'}
]

# Just to see what request looks like
# request(
#     method,
#     url,
#     params=url_params,
#     headers=headers_for_request,
#     verify=verify_ssl,
#     json=request_json,
#     data=request_data,
#     timeout=self._session_timeout,
#     proxies=proxies, # use different proxy not to be blocked
#     auth=auth_dict,
#     files=files_param
# )


def try_login(method, url, url_params, body_params, headers, basic_auth, use_json_in_body, verify_ssl):
    try:
        request_json = None
        request_data = None
        if body_params:
            request_json = body_params if use_json_in_body else None
            request_data = None if use_json_in_body else body_params

        response = _session.request(method, # GET or POST
                                    url,
                                    params=url_params,
                                    headers=headers,
                                    auth=basic_auth, # (Username, Password) tuple credentials
                                    data=request_data,
                                    json=request_json,
                                    verify=verify_ssl)

        if response.status_code in SUCCESS_STATUS_CODES:
            return True
    except Exception as e:
        print(f'Authentication Failed: {e}')

    return False


# Try all login methods possible for a single user
def try_logins(username, password, url):
    request_params = [
        {'Username': username, 'Password': password},
        {'username': username, 'password': password},
        {'login': username, 'Password': password},
        {'login': username, 'password': password},
        {'client_id': username, 'client_password': password},
        {'client_id': username, 'client_secret': password},
    ]

    for method, request_param, headers, use_json_in_body, use_url_params, verify_ssl in \
            itertools.product(METHODS, request_params, HEADERS, USE_JSON_IN_PARAMS,
                              USE_URL_PARAMS, VERIFY_SSL):

        url_params = request_param if use_url_params else None
        body_params = None if use_url_params else request_param

        success = try_login(method=method,
                            url=url,
                            url_params=url_params,
                            body_params=body_params,
                            headers=headers,
                            basic_auth=(username, password),
                            use_json_in_body=use_json_in_body,
                            verify_ssl=verify_ssl)
        if success:
            print(f'Successfully authenticatied!!'
                   f'method = {method},'
                   f'url_params = {url_params},'
                   f'params = {body_params},'
                   f'headers = {headers},'
                   # f'basic_auth = {basic_auth}'
                   f'use_json_in_body = {use_json_in_body}'
                   f'verify_ssl = {verify_ssl}')
            return success

    print('Failed to authenticate')
    return False


def test_all_users(combination_list, url):
    for username, password in combination_list:
        success = try_logins(username, password, url)
        if success:
            return True
        return False
