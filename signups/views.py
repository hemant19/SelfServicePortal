from django.shortcuts import render_to_response, RequestContext
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm


def Register(request):

    form = UserCreationForm()

    return render_to_response("signup.html",
                              locals(),
                              context_instance=RequestContext(request))
