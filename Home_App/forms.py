from django import forms
from Home_App.models import category_table, customer_table, food_table, reservation_table


from django import forms

#   ------ Category ---------- #

# class for edit category details at admin's end'
class CategoryEditForm(forms.Form):
    category_title = forms.CharField(label='Title', max_length=255)
    feature = forms.CharField(label='Features', max_length=255)

# class for add category at admin's end'
class CategoryForm(forms.ModelForm):
    class Meta:
        model = category_table
        fields = ['category_title','feature']


# ------- Customer -----------#
        
#class for edit customer details at admin's end
class CustomerEditForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=255)
    last_name = forms.CharField(label='Last Name', max_length=255)
    email_id = forms.CharField(label='Email Id',max_length=255)
    dob = forms.CharField(label='DOB',max_length=20)
    phone_no = forms.IntegerField(label='Ph No')
    user_id = forms.CharField(label='User Id',max_length=255)
    password = forms.CharField(label='Password',max_length=255)


#class for add customer at admin's end
class CustomerForm(forms.ModelForm):
    class Meta:
        model = customer_table
        fields = ['first_name','last_name','email_id','dob','phone_no','user_id','password']


# ------- Food Items -----------#
        
#class for edit customer details at admin's end
class FoodItemsEditForm(forms.Form):
    food_title = forms.CharField(label='Food Title', max_length=255)
    description = forms.CharField(label='Description', max_length=255)
    price = forms.IntegerField(label='Price')
    img_name = forms.CharField(label='Image Address',max_length=20)
    category_id = forms.IntegerField(label='Category id')
    feature = forms.CharField(label='Features',max_length=255)


#class for add customer at admin's end
class FoodItemsForm(forms.ModelForm):
    class Meta:
        model = food_table
        fields = ['food_title','description','price','img_name','category_id','feature']




# Reservation form at index.html
class ReservationForm(forms.ModelForm):
    class Meta:
        model = reservation_table
        fields = ['booking_name','time','total_person','date','message']