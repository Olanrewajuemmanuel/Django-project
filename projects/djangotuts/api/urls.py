from django.urls import include, path
from . import views
urlpatterns = [
    path("", views.index, name="home"),    
    path("register/", views.register, name="register"),
    path("articles/", views.ArticleAPIView.as_view(), name="articles"),
    path("articles/<int:id>/", views.ArticleDetail.as_view(), name="details")
]