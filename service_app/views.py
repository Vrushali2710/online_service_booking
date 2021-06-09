from typing import ContextManager
from django.shortcuts import HttpResponse,render
 
# Create your views here.

def index(request):
    context = {
        "variable" :"this is set"
    }
    # return HttpResponse("Hello, Cool IT Help!")
    return render(request,'index.html',context)


def about(request):
    # return HttpResponse("about")
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')

def contact(request):
    return render(request,'contact.html')
 

