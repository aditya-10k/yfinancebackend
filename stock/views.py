from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from datetime import datetime
import requests

def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def stock_list_view(request):
    url='https://yfinancebackend.onrender.com/api/stock/search/aap'
    response=requests.get(url)
    if response.status_code == 200:
        stocks = response.json()
    else:
        stocks=[]

    return render(request, 'search_stock.html', {'stocks': stocks})

def stock_detail_view(request):
    url = 'https://yfinancebackend.onrender.com/api/stock/IRFC.NS' 
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        data = {}

    return render(request, 'stock_detail.html', {'company': data})


def stock_news(request):
    url='https://yfinancebackend.onrender.com/api/stock/IRFC.NS/news/'
    response = requests.get(url)
    data = response.json()
    
    for item in data:
        timestamp = item.get("providerPublishTime")
        if timestamp:
            item["providerPublishTime"] = datetime.fromtimestamp(timestamp)

    return render(request, "stock_news.html", {"news_items": data})