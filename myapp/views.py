from django.shortcuts import render, redirect

from pyUFbr.baseuf import ufbr

from .models import Profile, Request
from django.http.request import HttpRequest
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as logoutt, login as loginn

from .forms import RegisterForm, RequestForm, LoginForm

from django.core.files.storage import FileSystemStorage

# Create your views here.

def redirect_index(request: HttpRequest):
    return redirect("index")

def index(request: HttpRequest):
    requests = Request.objects.all()

    data = []

    for req in requests:
        profile = Profile.objects.get(user_id=req.user.pk)
        checkImageExists(profile)
        data.append({"profile":profile,"request": req})

    return render(request, "myapp/index.html", context={"data": data})

def register(request: HttpRequest):
    form = RegisterForm()
    if request.POST:
        try:
            User.objects.get(username=request.POST.get("username"))
            form = RegisterForm(request.POST)
            form.add_error("username", "Este username já está em uso")
            return render(request, "myapp/register.html", context={"states": ufbr.list_uf, "form": form})
        except User.DoesNotExist:
            form = RegisterForm(request.POST)
            if form.is_valid:
                user = User.objects.create_user(
                    request.POST.get("username"),
                    request.POST.get("email"),
                    request.POST.get("password")
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
    return render(request, "myapp/register.html", context={"states": ufbr.list_uf, "form": form })

def login(request: HttpRequest):
    form = LoginForm()
    if request.POST:
        user = authenticate(
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user is not None:
            loginn(request, user)
            return redirect("index")
        else:
            form = LoginForm(request.POST)
    return render(request, "myapp/login.html", context={"form": form})

def logout(request: HttpRequest):
    logoutt(request)
    return redirect("index")

def request(request: HttpRequest):
    if request.user.is_authenticated:
        rq = None
        try:
            rq = Request.objects.get(user_id=request.user)
            if request.POST:
                rq.description = request.POST.get("description")
                rq.amount = request.POST.get("amount")
                rq.save()
        except Request.DoesNotExist:
            if request.POST:
                rq = Request.objects.create(
                    user_id = request.user.pk,
                    description = request.POST.get("description"),
                    amount = request.POST.get("amount")
                )
        form = RequestForm(initial={
            "description": rq.description,
            "amount": rq.amount
            }) if rq else RequestForm()
        return render(request, "myapp/request.html", context={"form": form})
    else:
        return redirect("login")


def verifyLink(link):
    if link[0:8] != "https://" and link[0:7] != "http://" and link != "":
        link = f"https://{link}"
    return link

def profile(request: HttpRequest):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user_id=request.user).get()
        checkImageExists(profile)
        if request.POST:
            if request.FILES:
                fss = FileSystemStorage()
                if profile.image:
                    if fss.exists(str(profile.image).split("/")[-1]):
                        fss.delete(str(profile.image).split("/")[-1])
                file = fss.save(request.user.pk, request.FILES.get("image"))
                profile.image = fss.url(file)
            
            profile.name = request.POST.get("name")
            profile.bio = request.POST.get("bio")
            profile.link_facebook = verifyLink(request.POST.get("link_facebook"))
            profile.link_instagram = verifyLink(request.POST.get("link_instagram"))
            profile.link_linkedin = verifyLink(request.POST.get("link_linkedin"))
            profile.link_youtube = verifyLink(request.POST.get("link_youtube"))
            profile.cellphone = request.POST.get("cellphone")
            profile.state = request.POST.get("state")
            profile.city = request.POST.get("city")
            profile.save()
        return render(request, "myapp/profile.html", context={"states": ufbr.list_uf, "cities": ufbr.list_cidades(profile.state), "profile": profile})
    else:
        return redirect("register")


def seeProfile(request):
    if request.GET:
        try:
            profile = Profile.objects.get(user_id=request.GET.get("user_id"))
            checkImageExists(profile)
            req = Request.objects.get(user_id=request.GET.get("user_id"))
            return render(request, "myapp/see_profile.html", context={"profile": profile, "request": req})
        except Profile.DoesNotExist:
            pass
    return redirect("index")


def checkImageExists(profile):
    print(profile.image)
    if not profile.image:
        return False
    fss = FileSystemStorage()
    if not fss.exists(str(profile.image).split("/")[-1]):
        profile.image = None
        profile.save()
        return False
    return True


def getCities(request):
    data = {"cities": ufbr.list_cidades(request.POST.get("state"))}
    return JsonResponse(data)
