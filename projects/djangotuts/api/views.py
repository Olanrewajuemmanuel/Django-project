# from django.shortcuts import render

# # Create your views here.

# from django.contrib.auth.models import User, Group
# from rest_framework import viewsets
# from rest_framework import permissions
# from api.quickstart.serializers import UserSerializer, GroupSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited
#     """
#     queryset  = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited
#     """
#     queryset  = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import ModelSerializer
from django import forms
from .models import User, Article
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class RegisterForm(forms.Form):
    """
    An abstract class for creating the register form
    for new users
    """
    url = forms.URLField(max_length=200, required=True)
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150)
    groups = forms.CharField(max_length=200)


def register(request):
    form = RegisterForm()
    errors = ""

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            u = User(**form.cleaned_data)
            u.save()
            print("Saved Successfully!")
            form = RegisterForm()
        else:
            errors = form.errors.as_data

    return render(request, "api/register.html", {
        'form': form,
        'errors': errors
    })


def index(*args, **kwargs):
    "Response for index page"
    return HttpResponse("Hello World")


class ArticleAPIView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ModelSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetail(APIView):

    def get_object(self, id):
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist or KeyError:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)



    def get(self, request, id):
        article = self.get_object(id)
        serializer = ModelSerializer(article)
        return Response(serializer.data)

    def put(self, request, id):
        article = self.get_object(id)
        serializer = ModelSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response("Your request has been updated", status=status.HTTP_200_OK)
        return JsonResponse(status=400)

    def delete(self, request, id):
        try:
            article = self.get_object(id)
            article.delete()
        except Article.DoesNotExist or KeyError:
            return HttpResponse(status=404)





@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == "GET":
        articles = Article.objects.all()
        serializer = ModelSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        # data = JSONParser().parse(request) #data is in request object and is parsed to JSON
        serializer = ModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # executed if method is_valid() fails
    else:
        return Response("Unsupported request type", status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE", 'PUT'])
def article_details(request, pk):
    "Method for getting specific info from API using an id in url params"
    try:
        article = Article.objects.get(pk=pk)
    except (Article.DoesNotExist or KeyError):
        return Response(f"No article with id: {pk}", status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        serializer = ModelSerializer(article)
        return Response(serializer.data)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = ModelSerializer(article, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response("Your request has been updated", status=status.HTTP_200_OK)
        return JsonResponse(status=400)
    elif request.method == "DELETE":
        article.delete()
        return HttpResponse(f"The specified article with id {pk} has been deleted")
    else:
        HttpResponse("Unsupported request type", status=400)
