from django.urls import path
from . import views

urlpatterns = [
    path('',views.landing_page_view, name='landing'),
    path('home/',views.home_page_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.stock_list_view, name='search'),
    path('stockdet/<str:symbol>/', views.stock_detail_view, name='stock_detail'),
    path('stocknews/', views.stock_news, name='stock_news'),
    path('financials/<str:symbol>/', views.stock_financials, name='stock_financials'),
    path('dividends/<str:symbol>/', views.stock_dividend, name='stock_dividends'),
]
