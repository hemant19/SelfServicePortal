from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def register(request):
    error = {}

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        try:
            if form.is_valid():
                username = request.POST.get("username")
                messages.info(request, username)
                form.save()
                return HttpResponseRedirect('/thankyou')
            else:
                if form.error_messages:
                    error['2'] = "password"
                else:
                    error['1'] = "username"

        except Exception as e:
            error['3'] = "password"
    else:
        form = UserRegistrationForm()
        form.error_messages.clear()

    return render_to_response("signup.html",
                              locals(),
                              context_instance=RequestContext(request))

def login_view(request):

    error = {}

    if request.method == 'POST':
        # messages.info(request, "in post")

        login_form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # messages.info(request, "in active user")

                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect('/viewvms/')
            else:
                # Return a 'disabled account' error message
                # messages.info(request, "in disabled user")
                error['1'] = 'disabled'
        else:
            # Return an 'invalid login' error message.
            # messages.info(request, "in invalid user")

            error['2'] = 'invalid'
    else:
        # messages.info(request, "not in post")
        login_form = AuthenticationForm()

    return render_to_response("login.html",
                              locals(),
                              context_instance=RequestContext(request))



def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/thankyou/')

def thankyou(request):

    return render_to_response("thankyou.html",
                              locals(),
                              context_instance=RequestContext(request))