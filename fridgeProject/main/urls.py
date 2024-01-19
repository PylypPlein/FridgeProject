from django.urls import path
from . import views
from .views import create_fridge, login_view,fridge_details,products_manage,add_to_fridge,modify_quantity
from django.contrib.auth import views as auth_views

app_name = 'main'
urlpatterns = [
    path('',views.home,name='home'),
    path('create_fridge/', create_fridge, name='create_fridge'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('fridge_details/<int:fridge_id>/', fridge_details, name='fridge_details'),
    path('products_manage/', products_manage, name='products_manage'),
    path('add_to_fridge/<int:product_id>/', add_to_fridge, name='add_to_fridge'),
    path('modify_quantity/<int:fridge_product_id>/', modify_quantity, name='modify_quantity'),
]