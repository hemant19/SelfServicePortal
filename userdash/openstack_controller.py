__author__ = 'Ashwini'
import time
import os
import uuid
import logging

import keystoneclient.v2_0.client as ksclient
import glanceclient.v2.client as glclient
from novaclient import client
from django.db.models import Q
from django.http import HttpResponse

from signups.credentials import get_keystone_creds, get_nova_creds
from models import *

error_logger = logging.getLogger('error')

def get_token():
    creds = get_keystone_creds()
    keystone = ksclient.Client(**creds)
    return keystone.auth_token

def authenticate(user_id):
    try:
        keystone_token = get_token()
        vuser_token = VcloudUserToken(auth_user=user_id, token = keystone_token)
        vuser_token.save()
        return HttpResponse({"status":"Success"})
    except Exception as e:
        error_logger.error('authenticate: %s', e)
        return HttpResponse({"status":"Failed"})

def create_instance(**kwargs):
    try:
        creds = get_nova_creds()
        nova = client.Client("2", **creds)
        key_name = kwargs['instance_name']+str(uuid.uuid1)
        private_key_filename = "/home/openstack/private_keys/"+key_name+".pem"
        private_key = None
        if not nova.keypairs.findall(name=key_name):
            keypair = nova.keypairs.create(name=key_name)
            fp = os.open(private_key_filename, os.O_WRONLY | os.O_CREAT, 0o600)
            print keypair.private_key
            private_key = keypair.private_key
            with os.fdopen(fp, 'w') as f:
                f.write(keypair.private_key)

        image = nova.images.find(name=kwargs['image_name'])
        flavor = nova.flavors.find(name=kwargs['flavor_name'])
        net = nova.networks.find(label="cf-net")
        nics = [{'net-id': net.id}]
        secgroup = nova.security_groups.find(name="default")
        instance = nova.servers.create(name=kwargs['instance_name'], image=image, flavor=flavor, key_name=key_name,
                                        nics=nics, security_groups=[secgroup.id] )

        # Poll at 5 second intervals, until the status is no longer 'BUILD'
        status = instance.status
        while status == 'BUILD':
            time.sleep(5)
            # Retrieve the instance again so the status field updates
            instance = nova.servers.get(instance.id)
            status = instance.status
        print "status: %s" % status

        # make entry in database:
        user_instance = VcloudUserInstances(auth_user= kwargs['user_id'], instance_id= instance.id, status= instance.status.upper())
        user_instance.save()

        #attach_ip_address
        floating_ips = nova.floating_ips.list()
        if not floating_ips:
            floating_ip = nova.floating_ips.create()
        else:
            floating_ip = floating_ips[0]
        instance.add_floating_ip(floating_ip)
        # ask the user to make  pem file named private_key_filename with private key as returned private key
        # Also give msg to use the command to do ssh
        return HttpResponse({'private_key':private_key, 'file_name':private_key_filename, 'status':'Success'})
    except Exception as e:
        error_logger.error('create_instance: %s', e)
        return HttpResponse({"status":"Failed"})


def get_instances(user_id):
    try:
        creds = get_nova_creds()
        nova = client.Client(**creds)
        instances = VcloudUserInstances.objects.filter(~Q(status='TERMINATED'), auth_user=user_id)
        instance_details = []
        for instance in instances:
            instance_info = {}
            current_instance = nova.servers.get(instance['instance_id'])
            if current_instance.status != 'TERMINATED':
                instance_info['name'] = current_instance.name
                instance_info['status'] = current_instance.status
                flavor = nova.flavors.get(current_instance.flavor['id'])
                instance_info['RAM'] = flavor.ram
                instance_info['Disk'] = flavor.disk
                instance_info['floating IP'] = current_instance.networks['cf-net'][1]
                instance_info['instance_id'] = instance['instance_id']
                instance_details.append(instance_info)
        return HttpResponse({'instance_details':instance_details, 'status':'Success'})
    except Exception as e:
        error_logger.error('get_instances: %s', e)
        return HttpResponse({"status":"Failed"})


def terminate_instance(user_id, instance_id):
    try:
        creds = get_nova_creds()
        nova = client.Client(**creds)
        instance = nova.servers.get(instance_id)
        instance.delete()
        vcloud_instance = VcloudUserInstances.objects.get(auth_user=user_id, instance_id=instance_id)
        vcloud_instance.status = 'TERMINATED'
        vcloud_instance.save()
        return HttpResponse({'status':'Success'})
    except Exception as e:
        error_logger.error('terminate_instance: %s', e)
        return HttpResponse({"status":"Failed"})


def start_instance(user_id, instance_id):
    try:
        vcloud_instance = VcloudUserInstances.objects.get(auth_user=user_id, instance_id=instance_id)
        vcloud_instance.status = 'ACTIVE'
        vcloud_instance.save()
        creds = get_nova_creds()
        nova = client.Client(**creds)
        nova.servers.start(instance_id)
        return HttpResponse({'status':'Success'})
    except Exception as e:
        error_logger.error('start_instance: %s', e)
        return HttpResponse({"status":"Failed"})


def stop_instance(user_id, instance_id):
    try:
        creds = get_nova_creds()
        nova = client.Client(**creds)
        nova.servers.stop(instance_id)
        vcloud_instance = VcloudUserInstances.objects.get(auth_user=user_id, instance_id=instance_id)
        vcloud_instance.status = 'SHUTOFF'
        vcloud_instance.save()
        return HttpResponse({'status':'Success'})
    except Exception as e:
        error_logger.error('stop_instance: %s', e)
        return HttpResponse({"status":"Failed"})


def list_flavors():
    try:
        creds = get_nova_creds()
        nova = client.Client(**creds)
        flavor_details = []
        flavors = nova.flavors.list()
        for flavor in flavors:
            flavor_info = {}
            flavor['flavor_name'] = flavor.name
            flavor_info['flavor_ram'] = flavor.ram
            flavor_info['flavor_disk'] = flavor.disk
            flavor_details.append(flavor_info)
        return HttpResponse({'flavors':flavor_details, 'status':'Success'})
    except Exception as e:
        error_logger.error('list_flavors: %s', e)
        return HttpResponse({"status":"Failed"})


def list_images():
    try:
        creds = get_keystone_creds()
        keystone = ksclient.Client(**creds)
        glance_endpoint = keystone.service_catalog.url_for(service_type='image',
        endpoint_type='publicURL')
        glance = glclient.Client(glance_endpoint, token=keystone.auth_token)
        images = glance.images.list()
        image_details = []
        for image in images:
            image_info = {}
            image_info['name'] = image.name
            image_details.append(image_info)
        return HttpResponse({'images':image_details, 'status':'Success'})
    except Exception as e:
        error_logger.error('list_images: %s', e)
        return HttpResponse({"status": "Failed"})


def get_vnc_console(instance_id):
    try:
        creds = get_nova_creds()
        nova = client.Client(**creds)
        console = nova.servers.get_vnc_console(instance_id)
        return HttpResponse({'console_url': str(console['console']['url']), 'status':'Success'})  # return url to user and ask him to open
    except Exception as e:
        error_logger.error('get_vnc_console: %s', e)
        return HttpResponse({"status":"Failed"})