from django.contrib import admin
from Home_App.models import category_table, food_table, order_table, admin_table, customer_table,Contact

admin.site.site_header = "Foodie | Admin"
# data in tabular form
# @admin.register(Contact)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = ['id','name','email']

# Register your models here.
admin.site.register((category_table, food_table, order_table, admin_table, customer_table,Contact))