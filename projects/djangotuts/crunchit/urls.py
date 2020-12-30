from django.urls import path

from . import views


app_name = 'crunchit'

urlpatterns = [
    path("", views.article_home_view, name="home"),
    path("shop", views.shop_view, name="shop"),
    path("add-product", views.query_view, name="search"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login, name="login"),
]
