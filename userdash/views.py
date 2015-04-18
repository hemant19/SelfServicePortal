from django.shortcuts import render_to_response, RequestContext

# Create your views here.
def createInstance(request):
    return render_to_response("create_instance.html",
                              locals(),
                              RequestContext(request))

def viewInstance(request):
    return render_to_response("view_instance.html",
                              locals(),
                              RequestContext(request))

def usageHistory(request):
    return render_to_response("usage_history.html",
                              locals(),
                              RequestContext(request))
