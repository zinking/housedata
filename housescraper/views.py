from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

import re
# Create your views here.



def render_any(request):
    return render(request, 'choices.html',{})

