#!/usr/bin/env python
"""
Pre-requisites for running this script:
- Running Openstack deployed using RDO

Reads 'keystonerc_admin' from root's Home folder and authenticates admin
then lists all the networks.

Run this script as a root user.

"""
import requests
import json
import os
import logging

from config import ADMINRC_PATH

# setting up logger
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def parse_rc(file_path):
    """Parses a RC file and extracts all the environment variable
    and its values and returns a dictionary.

    params: file_path: path to RC file
    return: dictionary with all environment variables as key and values
            as respective variable value.
    """
    if not os.path.exists(file_path):
        return None
    data = {}
    with open(file_path) as cred_file:
        lines = cred_file.readlines()
        for line in lines:
            words = line.split()
            # if blank line found
            if not words:
                continue
            if words[0] != 'export':
                continue
            # exclude word 'export' and split on '='
            key_value = ' '.join(words[1:]).split('=')
            data[key_value[0]] = key_value[1]
    return data


def extract_data(file_path):
    """Extract data from the RC file.

    params: file_path: path to file, containing data.
    return: url, username, password, tenant_name.
    """
    data = parse_rc(file_path)
    if not data:
        return None
    return (data.get('OS_AUTH_URL'),
            data.get('OS_USERNAME'),
            data.get('OS_PASSWORD'),
            data.get('OS_TENANT_NAME'))


def authenticate(url, username, password, tenant_name):
    """Authenticate user by communicating with server.

    params: url: url to authentication server api endpoint
    params: username: username of the user
    params: password: password of the user
    params: tenant_name: name of the tenant
    return: reply json data from server as a dict
    """
    url = os.path.join(url, 'tokens')
    data = {
            "auth": {
                "tenantName": tenant_name,
                "passwordCredentials": {
                    "username": username,
                    "password": password
                }
            }
    }
    try:
        reply = requests.post(url, data=json.dumps(data)).text
    except requests.exceptions.ConnectionError as e:
        logger.debug('[!] Error:', e)
        return None

    return json.loads(reply)


def list_networks(token):
    """Given an authentication token, here query is made to server for all
    networks present in this Openstack Instance.

    params: token: authentication token
    return: data returned by server in the dict form.
    """
    url = os.path.join('http://127.0.0.1:9696', 'v2.0/networks')
    headers = {'X-Auth-Token': token}
    try:
        reply = requests.get(url, headers=headers).text
    except requests.exceptions.ConnectionError as e:
        logger.debug('[!] Error:', e)
        return None

    return json.loads(reply)


def print_networks_info(networks):
    """Prints all the networks info in readable form.
    """
    print
    print 'Networks in this Openstack'
    if networks and networks.get('networks'):
        for network in networks.get('networks'):
            print '*'*20
            print 'Name: {}'.format(network['name'])
            print 'Id: {}'.format(network['id'])
            print 'Subnets: {}'.format(network['subnets'])
            print 'Tenant: {}'.format(network['tenant_id'])
            print 'Status: {}'.format(network['status'])


def main():
    data = extract_data(ADMINRC_PATH)
    if not data:
        msg = '[!] Error: Admin RC file does not exist or no data in file.'
        logger.debug(msg)
        return None
    reply = authenticate(*data)
    if reply and reply.get('access'):
        logger.debug('[ ] Authentication Successful.')
        logger.debug('[ ] Username: {}'.
                            format(reply['access']['user']['username']))
        logger.debug('[ ] UserID: {}'.format(reply['access']['user']['id']))
        networks = list_networks(reply['access']['token']['id'])
        print_networks_info(networks)

    elif reply and reply.get('error'):
        logger.debug('[!] Authentication Unsuccessful.')
        logger.debug('[!] Received code: {}'.format(reply['error']['code']))
    else:
        logger.debug('[!] Unknown error.')


if __name__ == '__main__':
    main()
