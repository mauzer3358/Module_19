from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from django.http import HttpResponse
from .forms import UserReg

# Create your views here.
def main_page(request):
    return render(request, 'main_template.html')

def shop_page(request):
    #games = ["Atomic Heart","Cyberpunk 2077", "PayDay 2"]
    games = Game.objects.all()
    context = {
        'games': games
    }
    return render(request, 'shop_template.html', context)

def cart_page(request):
    return render(request, 'cart_template.html')



# Create your views here.

def sign_up_by_html(request):
    #users = ['Tim', 'Tom']
    users = Buyer.objects.all()
    info = {}
    flag = 0

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')


        for user in users:
            if username not in user.name:
                continue
            else:
                info['error'] = 'Пользователь уже существует'
                flag = 1

        if flag == 0:
            if repeat_password != password:
                info['error'] = 'Пароли не совпадают'
            elif int(age) < 18:
                info['error'] = 'Вы должны быть старше 18'
            else:
                Buyer.objects.create(name=username, balance=0, age=age)
                info['OK'] = f'Приветствуем, {username}!'

    return render(request,'registration_page.html', context=info)





def sign_up_by_django(request):
    #users = ['Tim', 'Tom']
    users = Buyer.objects.all()
    info = {}
    flag = 0

    if request.method == 'POST':
        form = UserReg(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            print('username', username)
            print('pass', password)
            print('rep_pass', repeat_password)
            print('age', age)

            for user in users:
                if username not in user.name:
                    continue
                else:
                    info['error'] = 'Пользователь уже существует'
                    flag = 1

            if flag == 0:
                if repeat_password != password:
                    info['error'] = 'Пароли не совпадают'
                elif int(age) < 18:
                    info['error'] = 'Вы должны быть старше 18'
                else:
                    Buyer.objects.create(name=username, balance=0, age=age)
                    info['OK'] = f'Приветствуем, {username}!'
        return render(request, 'registration_page.html', context=info)
    else:
        form = UserReg()
        info['form'] = form

    return render(request, 'registration_page.html', context=info)