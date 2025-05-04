from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm, StockSearchForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from datetime import datetime,timezone
import requests

def landing_page_view(request):
    return render(request, 'landingPage.html')


def home_page_view(request):
    return render(request,'homePage.html')

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
            return redirect('/stock/search/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def stock_list_view(request):
    if request.method=='POST':
        form=StockSearchForm(request.POST)
        if form.is_valid():
            symbol=form.cleaned_data['symbol']

            url=f'https://yfinancebackend.onrender.com/api/stock/search/{symbol}'
            response=requests.get(url)
            if response.status_code == 200:
                stocks = response.json()
            else:
                stocks=[]
            return render(request, 'search_result_stock.html', {'stocks': stocks})
    else:
        form=StockSearchForm()
    return render(request, 'search_stock.html', {'form': form})


@login_required
def stock_detail_view(request,symbol):
    url = f'https://yfinancebackend.onrender.com/api/stock/{symbol}' 
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        data = {}

    return render(request, 'stock_detail.html', {'company': data})


@login_required
def stock_news(request):
    url='https://yfinancebackend.onrender.com/api/stock/IRFC.NS/news/'
    response = requests.get(url)
    data = response.json()
    
    for item in data:
        timestamp = item.get("providerPublishTime")
        if timestamp:
            item["providerPublishTime"] = datetime.fromtimestamp(timestamp)

    return render(request, "stock_news.html", {"news_items": data})


@login_required
def stock_financials(request, symbol):
    url = f'https://yfinancebackend.onrender.com/api/stock/{symbol}/financials'
    response = requests.get(url)

    if response.status_code == 200:
        financials_data = response.json()
    else:
        financials_data = {}

    years = []
    sample_metric = next(iter(financials_data.values()), {})
    for timestamp in sample_metric:
        if timestamp:
            try:
                dt = datetime.fromtimestamp(int(timestamp) / 1000, tz=timezone.utc)
                years.append(dt.year)
            except Exception:
                years.append("Invalid")
        else:
            years.append("N/A")

    return render(request, 'stock_financials.html', {
        'symbol':symbol,
        'financials_data': financials_data,
        'years': years,
    })


@login_required
def stock_dividend(request, symbol):
    url = f"https://yfinancebackend.onrender.com/api/stock/{symbol}/dividend"
    response = requests.get(url)
    dividend_data = {}

    if response.status_code == 200:
        raw_data = response.json()
        dividend_data = {
        datetime.fromtimestamp(int(ts) / 1000, tz=timezone.utc).strftime('%Y-%m-%d'): val
        for ts, val in raw_data.items()
        }      

    context = {
        "symbol": symbol.upper(),
        "dividends": sorted(dividend_data.items())
    }
    return render(request, 'stock_dividends.html', context)