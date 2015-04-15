from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm

def register(request):

    form = UserRegistrationForm(request.POST)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/thankyou')

    return render_to_response("signup.html",
                              locals(),
                              context_instance=RequestContext(request))

def login(request):

    login_form = AuthenticationForm(request.POST)

    return render_to_response("login.html",
                              locals(),
                              context_instance=RequestContext(request))

def thankyou(request):

    return render_to_response("thankyou.html",
                              locals(),
                              context_instance=RequestContext(request))