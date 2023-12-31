from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect, render
from .models import Article

def page_articles(request):
    return render(request, "articles.html", context={"posts": Article.objects.all()})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, "article_detail.html", {"post": post})
    except Article.DoesNotExist:
        return Http404

def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = {"text": request.POST["text"], "title": request.POST["title"]}
            if form["text"] and form["title"]:
                if not Article.objects.filter(title=form["title"]).exists():
                    Article.objects.create(
                        text=form["text"], title=form["title"], author=request.user
                    )
                    return redirect(
                        "article_detail", article_id=Article.objects.count()
                    )
                else:
                    form["errors"] = "Статья с таким названием уже существует"
                    return render(request, "create_post.html", {"form": form})
            else:
                form["errors"] = "Не все поля заполнены"
                return render(request, "create_post.html", {"form": form})
        else:
            return render(request, "create_post.html")
    else:
        raise Http404


def registred(request):
    if request.method == "POST":
        form = {
            "username": request.POST["username"],
            "email": request.POST["email"],
            "password": request.POST["password"],
        }
        if form["username"] and form["email"] and form["password"]:
            try:
                User.objects.get(username=request.POST["username"])
                form["errors"] = "Пользователь с таким именем уже существует"
                return render(request, "registrationpage.html", {"form": form})
            except User.DoesNotExist:
                User.objects.create_user(
                    username=request.POST["username"],
                    email=request.POST["username"],
                    password=request.POST["password"],
                )
                return redirect("logIn")
        else:
            form["errors"] = "Не все поля заполнены"
            return render(request, "registrationpage.html", {"form": form})
    else:
        return render(request, "registrationpage.html", {})


def login(request):
    if request.method == "POST":
        form = {
            "username": request.POST["username"],
            "password": request.POST["password"],
        }
        if form["username"] and form["password"]:
            user = authenticate(
                request,
                username=request.POST["username"],
                password=request.POST["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form["errors"] = "Введенный пользователь не существует"
                return render(request, "signinpage.html", {"form": form})
        else:
            form["errors"] = "Не все поля заполнены"
            return render(request, "signinpage.html", {"form": form})
    else:
        return render(request, "signinpage.html", {})


def logoutFunc(request):
    logout(request)
    return redirect("home")
