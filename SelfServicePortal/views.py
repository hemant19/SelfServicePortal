__author__ = 'hemant'
from django.shortcuts import render_to_response, RequestContext


def Index(request):
    return render_to_response("index.html",
                              locals(),
                              context_instance=RequestContext(request))
