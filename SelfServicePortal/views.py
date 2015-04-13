__author__ = 'hemant'
from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect

def index(request):

    return HttpResponseRedirect('/login/')
   # return render_to_response("index.html",
   #                           locals(),
   #                           context_instance=RequestContext(request))