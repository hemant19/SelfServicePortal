from django.shortcuts import render_to_response, RequestContext
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):

    form = UserRegistrationForm(request.POST)

    if form.is_valid():
        messages.info(request, "here")
        save_it = form.save(commit=False)
        save_it.save()
        messages.success(request, "Thank you for Joining")

    return render_to_response("signup.html",
                              locals(),
                              context_instance=RequestContext(request))

def login(request):

    login_form = AuthenticationForm(request.POST)

    return render_to_response("login.html",
                              locals(),
                              context_instance=RequestContext(request))