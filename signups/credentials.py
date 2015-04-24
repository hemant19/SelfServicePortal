__author__ = 'root'
# !/usr/bin/env python


def get_keystone_creds():
    d = {}
    # d['username'] = os.environ['OS_USERNAME']
    #  d['password'] = os.environ['OS_PASSWORD']
    #  d['auth_url'] = os.environ['OS_AUTH_URL']
    #  d['tenant_name'] = os.environ['OS_TENANT_NAME']

    d['username'] = 'cf'
    d['password'] = 'ADMIN'
    d['auth_url'] = 'http://192.168.18.7:35357/v2.0'
    d['tenant_name'] = 'cloudFoundry'
    return d


def get_nova_creds():
    d = {}
    # d['username'] = os.environ['OS_USERNAME']
    #  d['api_key'] = os.environ['OS_PASSWORD']
    #  d['auth_url'] = os.environ['OS_AUTH_URL']
    # d['project_id'] = os.environ['OS_TENANT_NAME']

    d['username'] = 'cf'
    d['api_key'] = 'ADMIN'
    d['auth_url'] = 'http://192.168.18.7:35357/v2.0'
    d['project_id'] = 'cloudFoundry'
    d['service_type'] = "compute"
    return d