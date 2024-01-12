from datetime import timezone
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from Home_App.models import Contact, customer_table, admin_table, category_table, food_table, reservation_table, cart_table, order_item_table
# from django.contrib.auth import get_user_model
# from django.core.exceptions import ObjectDoesNotExist
# from django.http import JsonResponse
from django.core import serializers
from Home_App.forms import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
import json
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel
import requests
import json
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
# Create your views here.

# for index.html

def index(request):
    return render(request,'index.html')

# for navbar pages

def contact(request):
    context={}
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        obj = Contact(name=name,email=email,message=message)
        obj.save()
        # return HttpResponse(f"Dear {name}, Thanks For yoour message")
        context['message'] = (f"Dear {name}, Thanks For yoour message")
        messages.success(request, f"Dear {name}, Thanks for your message")
    return render(request,'contact.html',context)

def blog(request):
    return render(request,'blog.html')
def about(request):
    return render(request,'about.html')
def cart(request):
    customer = customer_table.objects.get(user_id=request.user)
    cart_items = cart_table.objects.filter(customer_id=customer).select_related('food_id')
    print(cart_items)

    # customer = customer_table.objects.get(user_id=request.user)
    # orders = OrderModel.objects.filter(customer=customer)
    # d = []

    # for item in orders:
    #     d.push(item.order_id)

    # order_item = order_item_table.objects.filter(order_id__in = d)


    print(cart_items)

    return render(request,'cart.html',{ "cart": cart_items })

def cart_remove(request,cart_id):

    cart_table.objects.filter(cart_id=cart_id).delete()
    return redirect('cart')

def cart_quantity_add(request,cart_id):

    cart = cart_table.objects.get(cart_id=cart_id)
    cart.quantity = cart.quantity + 1
    cart.save()
    return redirect('cart')

def cart_quantity_remove(request,cart_id):

    cart = cart_table.objects.get(cart_id=cart_id)
    if cart.quantity > 1 :
        cart.quantity = cart.quantity - 1
        cart.save()
    return redirect('cart')



    # Obtain access token
def get_access_token():
    client_id = "AY2N4I3ri2td4gkHC3Ffp_keANUTeZfZCvkKycDpnMzR3TdjLK5Ze0-qN-nQsfdTJMmKsXkk0ohprBd9"
    client_secret = "EPsve_pcVXwPRcpp9ShJKqE7Um2X7AmT2i2QCW9f426JLeOUYCTwyEcWpWBOPiJ1jTbVmt9Wtyp39eZn"
    url = 'https://api-m.sandbox.paypal.com/v1/oauth2/token'
    data = {'grant_type': 'client_credentials'}
    auth = (client_id, client_secret)
    response = requests.post(url, data=data, auth=auth)
    return response.json().get('access_token')

def generate_order(request):
    
    access_token = get_access_token()

    customer = customer_table.objects.get(user_id=request.user)
    cartItems =cart_table.objects.filter(customer_id=customer)
    totalPrice = 0 
    print("sadfasd")

    for item in cartItems:
        totalPrice = totalPrice + (item.food_id.price * item.quantity)


    url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    data = {
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": totalPrice
                },
                "reference_id": "d9f80740-38f0-11e8-b467-0ed5f89f718b",
                "shipping": {
                    "address": {
                        "address_line_1": "123 Main St",
                        "address_line_2": "Apt 4",
                        "admin_area_2": "City",
                        "admin_area_1": "State",
                        "postal_code": "12345",
                        "country_code": "US"
                    }
                }
            }
        ],
        "intent": "CAPTURE",
        "payment_source": {
            "paypal": {
                "experience_context": {
                    "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                    "payment_method_selected": "PAYPAL",
                    "brand_name": "Foodie INC",
                    "locale": "en-US",
                    "landing_page": "LOGIN",
                    "shipping_preference": "SET_PROVIDED_ADDRESS",
                    "user_action": "PAY_NOW",
                    "return_url": "http://example.com/returnUrl",
                    "cancel_url": "http://example.com/cancelUrl"
                }
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    res = response.json()
    return JsonResponse(res)


def order_capture(request,paypal_order_id):

   # Retrieve data from the request body
    data = json.loads(request.body)

    # Extract required fields
    name = data.get('name')
    email = data.get('email')
    street = data.get('street')
    city = data.get('city')
    state = data.get('state')
    zip_code = data.get('zip_code')


    customer = customer_table.objects.get(user_id=request.user)
    cartItems =cart_table.objects.filter(customer_id=customer)

    print(name)
    print(email)
    print(street)
    print(city)
    print(state)
    print(paypal_order_id )
    print(request.user)

    order = OrderModel(price=0,customer=customer,name=name,email=email,street=street,city=city,state=state,zip_code=zip_code,paypal_order_id=paypal_order_id)
    order.save()
    order = OrderModel.objects.get(paypal_order_id=paypal_order_id)
    for item in cartItems:
        temp = order_item_table(food_id=item.food_id,order_id=order,quantity=item.quantity)
        temp.save()
        item.delete()
        order.price = order.price + (item.food_id.price * item.quantity)
    order.is_paid = True
    order.save()
    return JsonResponse({"res":"success"})


def shop(request):
    category = request.GET.get('category')
    print(category)
    food = food_table.objects.all()

    if category is not None:
        food = food.filter(category_id=category)


    food_json = serializers.serialize('json', food)
    return render(request,'shop.html',{"food": food_json, "category": category})


def reservation(request):
    return render(request,'reservation.html')


# for customers

class CustomLoginView(LoginView):
    def get_success_url(self):
        #  preserving the 'next' parameter if present
        redirect_url = self.request.GET.get('next','/')
        return super().get_success_url() + f'?next={redirect_url}' 



class CustomerTableBackend(ModelBackend):

    User = get_user_model()
    def add_to_cart(request,food_id):

        foodItem = food_table.objects.get(food_id=food_id)
        customer = customer_table.objects.get(user_id=request.user)


        try:
            cart_check = cart_table.objects.get(food_id=foodItem,customer_id=customer)
            cart_check.quantity = cart_check.quantity + 1
            cart_check.save()
        except cart_table.DoesNotExist:
            cartItem = cart_table(food_id=foodItem,customer_id=customer)
            cartItem.quantity = 1
            cartItem.save()
            print(cartItem)
           
            print("The cart item does not exist.")
        
        return HttpResponse("Success")
    

    # need to check
    def login_user(request):
        if request.method == 'POST':
            params = dict(request.POST)
            username = params['username'][0]
            password = params['pass1'][0]

            try:
                # # Check if the credentials are in the customer table or not
                # customer = customer_table.objects.get(user_id=username, password=password)
                
                # Use the authenticate method provided by Django
                user = authenticate(request, username=username, password=password)
                print("Authenticated as customer:", user)

                # Log in the user
                login(request, user)  # Specify the backend
                request.session['islogin'] = True
                print(request.user.id)
                fname = user.first_name
                return render(request, "index.html", {'fname': fname})

            except customer_table.DoesNotExist:
                # Handle invalid credentials

                print("thi sis exception")
                messages.error(request, "Invalid Credentials!")
                return redirect('index')

        return render(request, 'login.html')
        
 
User = get_user_model()
# For Admin auntheciation check krna hai
class AdminTableBackend(ModelBackend):
    def authenticate(self, request, user_name=None, password=None, **kwargs):
        try:
            #check if the credentials are in admin table or not
            admin_user = admin_table.objects.get(user_name=user_name, password=password)
            #creating a user instance using admin data
            user = User(
                id=admin_user.admin_id,
                username=admin_user.user_name,
                password=admin_user.password,
                # is_admin=admin_user.is_admin,
            )
            # user.is_admin = admin_user.is_admin
            # print("Authenticated as admin:", user)
            return user
        except admin_table.DoesNotExist:
            return None

    # for Admin login user 
        
    def login_user(request):
        if request.method == 'POST':
            user_name = request.POST.get('user_name')
            password = request.POST.get('password')

            # Using custom authentication method
            user = authenticate(request, username=user_name, password=password)


            if user is not None:
                # User credentials are correct, then log in the user
                login(request, user)
                return render(request, "admin-dashboard.html", {'user_name': user_name})
            
            else:
                # User credentials are incorrect, display an error message
                messages.error(request, "Invalid Credentials!")
                return redirect('index')
        
        return render(request, 'admin-login.html')
    


def signup(request):
    if request.method=="POST":
        username = request.POST['username'] #login -> email paswd
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        dob = request.POST['dob']
        phone_no = request.POST['phone_no']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return render(request,'signup')

       

        new_customer = customer_table (
            first_name=fname,
            last_name=lname,
            email_id=email,
            dob=dob,
            phone_no=phone_no,
            user_id=username,
            password=pass1,
        )

        # myuser.save()
        new_customer.save()

        messages.success(request, "Your Account has been successfully created")

        return redirect('/login')
    
    return render(request, 'signup.html')



def signout(request):
    context={}
    logout(request)
    request.session['islogin'] = False
    context['message'] = ("Logged out successfully")
    messages.success(request, "Logged out successfully")
    return render(request,'index.html',context)


def index(request):
    if request.user.is_authenticated:
        fname = request.user.first_name
        return render(request, 'index.html', { 'fname': fname})
    else:
        return render(request, 'index.html')


def adminLogin(request):

    # if request.method == 'POST':

    return render(request,'admin-login.html')

def adminDashboard(request, section=None):
    section_template = {
        'categories': 'admin-dashboard-category.html',
        'customers': 'admin-dashboard-customers.html',
        'foodItems': 'admin-dashboard-foodItems.html',
        'reservation':'admin-dashboard-reservation.html',
        'recentOrders': 'admin-dashboard-recentOrders.html'
    }
    template_name = section_template.get(section, 'admin-dashboard.html')
    # return render(request,template_name)

    categories = category_table.objects.all()
    category_count = category_table.objects.count()
    foodItems = food_table.objects.all()
    foodItem_count = food_table.objects.count()
    customers = customer_table.objects.all()
    customer_count=customer_table.objects.count()
    reservation=reservation_table.objects.all()
    return render(request, template_name, {'categories':categories, 'categoryCount':category_count, 'foodItems':foodItems, 'food_item_count':foodItem_count, 'customers':customers, 'customerCount':customer_count, 'reservations':reservation})



#  CRUD Operation at Admin-Dashboard

# ---------- Customer ----------
def edit_customer(request,customer_id):
    customer = get_object_or_404(customer_table,customer_id=customer_id)
    if request.method == 'POST':
        form = CustomerEditForm(request.POST)
        if form.is_valid():
            #updating customer details
            customer.first_name=form.cleaned_data['first_name']
            customer.last_name=form.cleaned_data['last_name']
            customer.email_id=form.cleaned_data['email_id']
            customer.dob=form.cleaned_data['dob']
            customer.phone_no=form.cleaned_data['phone_no']
            customer.user_id=form.cleaned_data['user_id']
            customer.password=form.cleaned_data['password']
            customer.save()
            return redirect(reverse('admin-dashboard-section',kwargs={'section':'customers'}))
    else:
            form = CustomerEditForm(initial={
                'first_name':customer.first_name,
                'last_name':customer.last_name,
                'email_id':customer.email_id,
                'dob':customer.dob,
                'phone_no':customer.phone_no,
                'user_id':customer.user_id,
                'password':customer.password
            })

    return render(request,'admin-dashboard-customer-edit-modal.html',{'form':form,'customer_id':customer_id})
    
def delete_customer(request,customer_id):
    customer = get_object_or_404(customer_table,customer_id=customer_id)
    customer.delete()
    return redirect(reverse('admin-dashboard-section',kwargs={'section':'customers'}))

def add_customer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('admin-dashboard-section',kwargs={'section':'customers'}))
    return render(request,'admin-dashboard-customer-add.html',{'form':form})

    

# ---------- Category ----------    
def edit_category(request, category_id):
    category = get_object_or_404(category_table, category_id=category_id)

    if request.method == 'POST':
        form = CategoryEditForm(request.POST)
        if form.is_valid():
            # Update category fields based on form data
            category.category_title = form.cleaned_data['category_title']
            category.feature = form.cleaned_data['feature']
            category.save()

            # display success message
            messages.success(request, ' Category details updated successfully.')
            return redirect(reverse('admin-dashboard-section',kwargs={'section':'categories'}))  
    else:
        form = CategoryEditForm(initial={
            'category_title': category.category_title,
            'feature': category.feature,
        })

    return render(request, 'admin-dashboard-category-edit-modal.html', {'form': form, 'category_id': category_id})


def delete_category(request, category_id):
    category = get_object_or_404(category_table,category_id=category_id)
    category.delete()

    # displaying message
    messages.success(request,'Category deleted successfully.')
    return redirect(reverse('admin-dashboard-section', kwargs={'section':'categories'}))


def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Category added successfully')
            return redirect(reverse('admin-dashboard-section', kwargs={'section':'categories'}))
        
    return render(request,'admin-dashboard-category-add.html',{'form':form})


# ---------- Food Items ----------    
def edit_foodItems(request, food_id):
    food = get_object_or_404(food_table, food_id=food_id)

    if request.method == 'POST':
        form = FoodItemsEditForm(request.POST)
        if form.is_valid():
            # Update category fields based on form data
            food.food_title = form.cleaned_data['food_title']
            food.description = form.cleaned_data['description']
            food.price = form.cleaned_data['price']
            food.img_name = form.cleaned_data['img_name']
            category_id = form.cleaned_data['category_id']
            category = get_object_or_404(category_table,category_id=category_id)
            food.category_id=category
            food.feature = form.cleaned_data['feature']
            food.save()

            # display success message
            return redirect(reverse('admin-dashboard-section',kwargs={'section':'foodItems'}))  
    else:
        form = FoodItemsEditForm(initial={
            'food_title': food.food_title,
            'description': food.description,
            'price': food.price,
            'img_name': food.img_name,
            'category_id': food.category_id,
            'feature': food.feature,
        })

    return render(request, 'admin-dashboard-foodItems-edit-modal.html', {'form': form, 'food_id': food_id})


def delete_foodItems(request, food_id):
    food = get_object_or_404(food_table,food_id=food_id)
    food.delete()
    return redirect(reverse('admin-dashboard-section', kwargs={'section':'foodItems'}))


def add_foodItems(request):
    form = FoodItemsForm()
    if request.method == 'POST':
        form = FoodItemsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('admin-dashboard-section', kwargs={'section':'foodItems'}))
        
    return render(request,'admin-dashboard-foodItems-add.html',{'form':form})

# order

class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(
            category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        
        return render(request, 'order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        order.items.add(*item_ids)

        # After everything is done, send confirmation email to the user
        body = ('Thank you for your order! Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'order_pay_confirmation.html')



#  ----- Reservation -----
def approve_reservation_request(request, reservation_id):
    reservation = get_object_or_404(reservation_table, reservation_id=reservation_id)
    reservation.status='approved'
    reservation.save()
    return redirect(reverse('admin-dashboard-section',kwargs={'section':'reservation'}))

def deny_reservation_request(request,reservation_id):
    reservation = get_object_or_404(reservation_table,reservation_id=reservation_id)
    reservation.status='denied'
    reservation.save()
    return redirect(reverse('admin-dashboard-section',kwargs={'section':'reservation'}))


def make_reservation(request):
    form = ReservationForm()
    if request.method == 'POST':
        form =  ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'/login', {'form':form})

# def make_reservation(request):   #at index.html (customer's end)
#     if request.method == 'POST':
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             reservation = form.save(commit=False)

#             if 'customer_id' in request.session:
#                 customer_id = request.session['customer_id']

#                 try:
#                     customer = customer_table.objects.get(customer_id=customer_id)
#                     reservation.customer_id = customer  # setting cutomer id based on the logged in user
#                     reservation.save()
#                     return render(request,'index.html', {'reservation_success':True})
#                 except customer_table.DoesNotExist:
#                     pass
#             else:
#                 return render(request, 'index.html', {'form':form, 'authentication_error':True})
#         else:
#             print(form.errors)
#     else:
#         form = ReservationForm()
    
#     return render(request,'index.html', {'form':form})


# def make_reservation(request):   #at index.html (customer's end)
#     if request.method == 'POST':
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             reservation = form.save(commit=False)
#             customer_table = request.user.customer_table
#             reservation.customer_id = customer_table  # setting cutomer id based on the logged in user
#             reservation.save()
#             return render(request,'index.html', {'reservation_success':True})
#         else:
#             print(form.errors)
#     else:
#         form = ReservationForm()
    
#     return render(request,'index.html', {'form':form})

# def make_reservation(request):   #at index.html (customer's end)
#     if request.user.is_authenticated:
#         print("user is authenticated")
#         if request.method == 'POST':
#             form = ReservationForm(request.POST)
#             if form.is_valid():
#                 reservation = form.save(commit=False)
#                 reservation.customer_id = request.user   # setting cutomer id based on the logged in user
#                 reservation.save()
#                 return render(request,'index.html', {'reservation_success':True})
#             else:
#                 print(form.errors)
#         else:
#             form = ReservationForm()
    
#         return render(request,'index.html', {'form':form})
#     else:
#         return redirect('login')