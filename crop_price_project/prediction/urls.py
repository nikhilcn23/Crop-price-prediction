from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    path('', views.index, name='index'),
    path('get-districts/', views.get_districts, name='get_districts'),
    path('get-markets/', views.get_markets, name='get_markets'),
    path('predict/', views.predict_price, name='predict_price'),
]