from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm

# Create your models here.

#Category
class category_table(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_title = models.CharField(max_length=55)
    img_name = models.CharField(max_length = 55)
    feature = models.CharField(max_length = 90)

    def __str__(self):
        return str(self.category_id)
    
#contact table
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    added_on = models.DateTimeField(auto_now_add = True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Contact Table'

#Order
class order_table(models.Model):
    order_id = models.AutoField(primary_key=True)
    # food_title = models.CharField(primary_key=True, max_length=20)
    category_id=models.ForeignKey(category_table,on_delete=models.CASCADE)
    price = models.IntegerField()
    qty = models.IntegerField()
    total = models.IntegerField()
    date = models.DateField()
    status = models.CharField(max_length=20)
    cust_name = models.CharField(max_length=20)
    cust_contact = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d+$', #regex for only numeric digits
                message='Phone number must contain only numeric digits.',
                code='invalid phone number'
            ),
        ]
    )


#Food
class food_table(models.Model):
    food_id = models.AutoField(primary_key=True)
    food_title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    price = models.IntegerField()
    img_name = models.CharField(max_length=20)
    category_id = models.ForeignKey(category_table,on_delete=models.CASCADE)
    feature = models.CharField(max_length=20)
    


#Admins 
class admin_table(models.Model):
    is_admin = models.BooleanField(default=True)
    admin_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=20)
    user_name = models.CharField(max_length=30)
    password = models.CharField(max_length=50)

# Customer Table
class customer_table(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email_id = models.CharField(max_length=50)
    dob = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=10)
    user_id = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return str(self.customer_id)



# Reservation Table
class reservation_table(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    # customer_id = models.ForeignKey(customer_table,on_delete=models.CASCADE)
    booking_name=models.CharField(max_length=40)
    date = models.DateField()
    time = models.TimeField()
    total_person=models.IntegerField()
    message=models.CharField(max_length=255)
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('approved','Approved'),
        ('denied','Denied'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Reservation {self.reservation_id} for {self.customer_id} at {self.date} {self.time} - Status: {self.status}"



# Cart Table
class cart_table(models.Model):
    cart_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(customer_table,on_delete=models.CASCADE)
    food_id = models.ForeignKey(food_table,on_delete=models.CASCADE,related_name='food_set')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.cart_id)
    



    
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OrderModel(models.Model):
    order_id = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    customer = models.ForeignKey(customer_table,on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=15, blank=True)
    zip_code = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'

# order Items  Table
class order_item_table(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(OrderModel,on_delete=models.CASCADE)
    food_id = models.ForeignKey(food_table,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.cart_id)
    