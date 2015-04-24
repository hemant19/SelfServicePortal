import re

from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from django.contrib import messages

from openstack_controller import create_instance, get_instances, terminate_instance, start_instance, stop_instance, \
    get_vnc_console

# Create your views here.
def createInstanceView(request):
    current_user = request.user
    error = {}

    print current_user.id
    if not current_user.is_authenticated():
        HttpResponseRedirect('/error')

    if request.method == 'POST':
        instance = request.POST.get('instance_name')
        flavor = request.POST.get('flavor')
        image = request.POST.get('os')
        uid = current_user

        image = 'Ubuntu-trusty'
        flavor = 'm1.small'
        if re.match('^[a-zA-Z][a-zA-Z0-9_-]+$', instance):
            ret_val = create_instance(instance_name=instance, flavor_name=flavor, image_name=image, user_id=uid)

            if ret_val['status'] == 'Success':
                if ret_val['private_key']:
                    messages.info("Private key" + ret_val['private_key'])

                messages.info(request, "Instance Created .....")
                return HttpResponseRedirect('/viewvms/')
            else:
                return errorResponse(request, 'Cloud not create instance ...some error occured')

        else:
            error['instance_name'] = 'Please insert a valid username'

    return render_to_response("create_instance.html",
                              locals(),
                              RequestContext(request))

def viewInstance(request):
    current_user = request.user
    error = {}

    print current_user.id
    if not current_user.is_authenticated():
        HttpResponseRedirect('/error')

    ret_val = get_instances(current_user)

    if ret_val['status'] == 'Success':
        instance_list = ret_val['instance_details']
    else:
        return errorResponse(request, 'Some error Occured')

    return render_to_response("view_instance.html",
                              locals(),
                              RequestContext(request))

def usageHistory(request):
    return render_to_response("usage_history.html",
                              locals(),
                              RequestContext(request))


def terminateInstanceView(request):
    current_user = request.user

    if not current_user.is_authenticated():
        HttpResponseRedirect('/error')

    inst_id = request.GET.get('instanceid')

    ret_val = terminate_instance(user_id=current_user, instance_id=inst_id)

    if ret_val['status'] == 'Success':
        messages.info(request, "Image successfully terminates")
        return HttpResponseRedirect('/viewvms/')
    else:
        return errorResponse(request, 'There was a problem terminating the image')


def stopInstanceView(request):
    current_user = request.user

    if not current_user.is_authenticated():
        HttpResponseRedirect('/error')

    inst_id = request.GET.get('instanceid')

    ret_val = stop_instance(user_id=current_user, instance_id=inst_id)

    if ret_val['status'] == 'Success':
        messages.info(request, "Image successfully stopped")
        return HttpResponseRedirect('/viewvms/')
    else:
        return errorResponse(request, 'There was a problem stopping the image')


def viewConsole(request):
    current_user = request.user

    if not current_user.is_authenticated():
        HttpResponseRedirect('/error')

    inst_id = request.GET.get('instanceid')

    ret_val = get_vnc_console(inst_id)
    if ret_val['status'] == 'Success':
        vnc_url = ret_val['console_url']
        return HttpResponseRedirect(vnc_url)

    messages.error(request, "Sorry cannot open vnc console")
    return HttpResponseRedirect('/viewvms/')


def startInstanceView(request):
    current_user = request.user

    if not current_user.is_authenticated():
        HttpResponseRedirect('/error')

    inst_id = request.GET.get('instanceid')

    ret_val = start_instance(user_id=current_user, instance_id=inst_id)

    if ret_val['status'] == 'Success':
        messages.info(request, "Image successfully started")
        return HttpResponseRedirect('/viewvms/')
    else:
        return errorResponse(request, 'There was a problem stopping the image')


def errorResponse(request, err):
    return render_to_response("u_error.html", locals(), RequestContext(request));
