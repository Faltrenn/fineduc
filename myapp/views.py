from django.shortcuts import render, redirect

from pyUFbr.baseuf import ufbr

from .models import Profile
from django.http.request import HttpRequest
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as logoutt, login as loginn

from .forms import RegisterForm

# Create your views here.

def redirect_index(request: HttpRequest):
    return redirect("index")

def index(request: HttpRequest):
    return render(request, "myapp/index.html", context={"data": range(5)})

def register(request: HttpRequest):
    if request.POST:
        try:
            User.objects.get(username=request.POST.get("username"))
            return render(request, "myapp/register.html", context={"states": ufbr.list_uf, "form": RegisterForm(request.POST)})
        except User.DoesNotExist:
            form = RegisterForm(request.POST)
            if form.is_valid:
                user = User.objects.create_user(
                    request.POST.get("username"),
                    request.POST.get("email"),
                    request.POST.get("pass")
                )

                Profile.objects.create(
                    user_id = user.pk,
                    name = request.POST.get("name"),
                    cellphone = request.POST.get("cellphone"),
                    state = request.POST.get("state"),
                    city = request.POST.get("city"),
                )

                loginn(request, user)
                return redirect("index")
            else:
                print("form errado")
    else:
        return render(request, "myapp/register.html", context={"states": ufbr.list_uf, "form": RegisterForm() })

def login(request: HttpRequest):
    if request.POST:
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("pass"))
        if user is not None:
            loginn(request, user)
            return redirect("index")
    return render(request, "myapp/login.html")

def logout(request: HttpRequest):
    logoutt(request)
    return redirect("index")

def request(request: HttpRequest):
    if not request.user.is_authenticated:
        return render(request, "myapp/request.html")
    else:
        return redirect("register")

def profile(request: HttpRequest):
    if request.user.is_authenticated:
        return render(request, "myapp/profile.html", context={"states": ufbr.list_uf})
    else:
        return redirect("register")

def getCities(request):
    data = {"cities": ufbr.list_cidades(request.POST.get("state"))}
    return JsonResponse(data)
