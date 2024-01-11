
from django.contrib import admin
from django.urls import path, include
from Home_App import views as hv

urlpatterns = [
    path('home/',hv.index, name='home'),  
    path('',hv.index, name='index'),  
    path('contact/',hv.contact,name="contact"),
    path('blog/',hv.blog,name='blog'),
    path('about/',hv.about,name='about'),
    path('shop/',hv.shop,name='shop'),
    path('reservation/',hv.reservation,name='reservation'),
    path('dj-admin/', admin.site.urls),
    path('login/',hv.CustomerTableBackend.login_user, name='login'),
    path('login-admin/',hv.AdminTableBackend.login_user, name='login-admin'),
    path('signup/',hv.signup, name='signup'),
    path('signout/',hv.signout, name='signout'),
    # path('index/',hv.index, name='index'),
    path('admin-login/',hv.adminLogin, name='admin-login'),
    path('approve-reservation/<int:reservation_id>/', hv.approve_reservation_request, name='approve_reservation_request'),
    path('deny-reservation/<int:reservation_id>/', hv.deny_reservation_request, name='deny_reservation_request'),
    path('admin-dashboard/',hv.adminDashboard, name='admin-dashboard'),
    path('admin-dashboard/<str:section>/',hv.adminDashboard, name='admin-dashboard-section'),
    path('admin-dashboard-category-edit/<int:category_id>/',hv.edit_category, name='edit_category'),
    path('admin-dashboard-category-delete/<int:category_id>/',hv.delete_category,name='admin-dashboard-category-delete'),
    path('admin-dashboard-category-add/',hv.add_category,name='admin-dashboard-category-add'),
    path('admin-dashboard-customer-edit/<int:customer_id>/',hv.edit_customer,name='edit_customer'),
    path('admin-dashboard-customer-delete/<int:customer_id>/',hv.delete_customer,name='delete_customer'),
    path('admin-dashboard-customer-add/',hv.add_customer,name='admin-dashboard-customer-add'),
    path('admin-dashboard-foodItems-edit/<int:food_id>/',hv.edit_foodItems,name='edit_food'),
    path('admin-dashboard-foodItems-delete/<int:food_id>/',hv.delete_foodItems,name='delete_food'),
    path('admin-dashboard-foodItems-add/',hv.add_foodItems,name='admin-dashboard-foodItems-add'),

    # Need to ask
    
    path('make_reservation/', hv.make_reservation, name='make_reservation'),
    

    # path('newHome/',hv.newHome, name='newHome'),

]