from django.shortcuts import render_to_response, RequestContext
from .forms import UserRegistrstionForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


def register(request):

    form = UserRegistrstionForm(request.POST)

    if form.is_valid():
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