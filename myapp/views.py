from django.shortcuts import render, redirect

from pyUFbr.baseuf import ufbr

# Create your views here.

def redirect_index(request):
    return redirect("index")

def index(request):
    return render(request, "myapp/index.html", context={"data": range(5)})

def register(request):
    return render(request, "myapp/register.html", context={"states": ufbr.list_uf})

def login(request):
    return render(request, "myapp/login.html")

def request(request):
    if not request.user.is_authenticated:
        return render(request, "myapp/request.html")
    else:
        return redirect("register")

def profile(request):
    if not request.user.is_authenticated:
        return render(request, "myapp/profile.html", context={"states": ufbr.list_uf})
    else:
        return redirect("register")
