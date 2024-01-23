from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


from web.forms import *
from web.models import *

@login_required
def main_view(request):
    news = News.objects.all()

    total_count = news.count()

    paginator = Paginator(news, per_page=3)
    page_number = request.GET.get("page", 1)
    return render(request, "web/main.html", {
        'news': paginator.get_page(page_number),
        'total_count': total_count,
    })

def news_add_view(request):
    form = NewsForm()
    if request.method == 'POST':
        form = NewsForm(data=request.POST, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect("main")
    return render(request, "web/news_create.html", {
        "form": form
    })

def news_delete_view(request, id):
    news = get_object_or_404(News, id=id)
    news.delete()
    return redirect('main')





def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )

            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
    return render(request, "web/registration.html", {
        "form": form,
        "is_success": is_success
    })


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, 'Неправильный логин или пароь')
            else:
                login(request, user)
                return redirect("main")
    return render(request, 'web/auth.html', {
        "form": form
    })


def logout_view(request):
    logout(request)
    return redirect("main")



