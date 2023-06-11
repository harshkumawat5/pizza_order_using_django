from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth import login,logout,authenticate


from django.contrib.auth.decorators import login_required
# Create your views here.

from django.conf import settings
from instamojo_wrapper import Instamojo
api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN,endpoint="https://test.instamojo.com/api/1.1/")

def home(request):
    pizzas=Pizza.objects.all()
    context={'pizzas':pizzas}
    return render(request,'home.html',context)

def login_page(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)
        if not user.exists:
            messages.add_message(request, messages.INFO, "Not registered")
            return redirect('/api/login/')
        
        user=authenticate(username=username,
                          password=password)
        
        if user is None:
            messages.add_message(request, messages.INFO, "Credentials are not correct")
        else:
            login(request,user)
            return redirect('/api/home/')

    return render(request,'login_page.html')
    

def register_page(request):
    if request.method=="POST":
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        password=request.POST.get('password')
        email=request.POST.get('email')

        user=User.objects.filter(username=username)
        if user.exists():
            messages.add_message(request, messages.INFO, "Username already exists")
            return redirect('/api/register/')
        
        user=User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        user.set_password(password)
        user.save()

        messages.add_message(request, messages.INFO, "Account created successfully")
        return redirect('/api/register/')

    return render(request,'register_page.html')


@login_required(login_url='/api/login')
def add_cart(request,pizza_uid):
    user=request.user

    pizza_obj=Pizza.objects.get(uid=pizza_uid)
    cart,_=Cart.objects.get_or_create(user=user,is_paid=False)

    cart_items=CartItems.objects.create(
        cart=cart,
        pizza=pizza_obj
    )

    return redirect('/api/home/')

@login_required(login_url='/api/login')
def cart(request):
    cart=Cart.objects.get(is_paid=False,user=request.user)
    if cart.get_cart_total():
        response=api.payment_request_create(
            amount=cart.get_cart_total(),
            purpose='Order',
            buyer_name=request.user.username,
            email=request.user.email,
            redirect_url="http://127.0.0.1:8000/api/success"
        )
        cart.instamojo_id=response['payment_request']['id']
        cart.save()
        context={'carts':cart,'payment_url':response['payment_request']['longurl']}
        return render(request,'cart.html',context)
    else:
        context={'carts':cart}
        return render(request,'cart.html',context)

@login_required(login_url='/api/login')
def remove_cart_item(request,cart_item_uid):
    try:
        CartItems.objects.get(uid=cart_item_uid).delete()
        return redirect('/api/cart/')
    except Exception as e:
        print(e)

@login_required(login_url='/api/login')
def orders(request):
    orders=Cart.objects.filter(is_paid=True,user=request.user)
    context={'orders':orders}
    return render(request,'orders.html',context)

@login_required(login_url='/api/login')
def success(request):
    payment_request=request.GET.get('payment_request_id')
    cart=Cart.objects.get(instamojo_id=payment_request)
    cart.is_paid=True
    cart.save()
    return redirect('/api/orders/')


def logout_page(request):
    logout(request)
    return redirect('/api/login/')