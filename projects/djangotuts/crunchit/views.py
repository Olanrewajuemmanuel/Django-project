from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Product, Users
from django.urls import reverse
from .forms import UserForm, LoginForm
# Create your views here.

def index_view(request):
    try:
       product_data = Product.objects.order_by("-amount_sold")[:5]
       top_products = []
       for product in product_data:
           if product.top_selling():
               top_products.append(product)


       all_products = Product.objects.all()
       featured_products = []
       for product in all_products:
           if product.featured is True:
               featured_products.append(product)

    except Product.DoesNotExist:
        return Http404("No top selling product")
    context = {
        'product_data': top_products,
        'featured': featured_products[:5]
    }

    return render(request, "home.html", context)

def shop_view(request):
    try:
        product_data = Product.objects.order_by("-featured")

    except Product.DoesNotExist or KeyError:
        Http404("No Item in shop")

    context = {
        'list': product_data
    }

    return render(request, "shop.html", context)

def query_view(request):
    search = request.GET['search'].strip()

    try:
        searched_product = Product.objects.get(item_name = search)


    except Product.DoesNotExist:
        return HttpResponse(f"We could not find any records matching the key word '{search}'")

    return HttpResponse(str(searched_product) + " was Found in store, buy here: http://localhost:8000/crunchit/shop ")

def register_view(request):
    my_form = UserForm()

    if request.method == "POST":
        my_form = UserForm(request.POST)
        if my_form.is_valid():
            validated_data = my_form.cleaned_data
            u = Users(**validated_data)
            u.save()
            my_form = UserForm()
        else:
            print(my_form.errors)




   
    context = {
        'form': my_form
    }
    return render(request, "new.html", context)

def login(request):
    form = LoginForm()

    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            form_email = form.cleaned_data['email']
            email = Users.objects.filter(email=form_email)
            print(email)
    return render(request, "loggedin.html", {
        'form': form
    })


