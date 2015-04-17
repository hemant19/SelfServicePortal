__author__ = 'Ashwini'
import keystoneclient.v2_0.client as ksclient
from signups.credentials import get_keystone_creds

def get_token():
    creds = get_keystone_creds()
    keystone = ksclient.Client(**creds)
    return keystone.auth_token

def authenticate(user):
    keystone_token = get_token()
