import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import DurationField
from .manager import UserManager
from django.urls import reverse

# from django.core.validators import User

# from django.utils import timezone

# Create your models here.
class Vehicle(models.Model):
    id = models.UUIDField(primary_key= True,default=uuid.uuid4, editable=False)
    name = models.CharField(("Name of Vehicle"), blank=True, max_length=255)
    type = models.CharField(("Type of Vehicle"), blank=True, max_length=255)
    fuel_type = models.CharField(blank=True, max_length=255)
    chassis_no =models.CharField(blank=True, max_length=255)
    is_active = models.BooleanField(default=False)
    image = models.ImageField(upload_to = "vehicle/images",default = "")

    def __str__(self):
        return self.name

class Model (models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    # Vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    name = models.CharField(blank=True,max_length=255)
    is_active = models.BooleanField(default=False)
class Categorie(models.Model):
    name = models.CharField(("Name of Category"), blank=True, max_length=255)
    slug = models.SlugField(unique=True )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('service_app:service_category', args=[self.slug])
    # def get_all_services_by_id(categorie_id):
    #     if categorie_id:
    #         return Service.objects.filter(categorie =categorie_id)
    #     else:
    #         return Service.objects.all()



class Service(models.Model):
    name = models.CharField(("Name of Service"), blank=True, max_length=255) 
    Duration = models.CharField(blank=True,max_length=30)
    Warranty = models.CharField(blank=True,max_length=30)
    what_included = models.CharField( blank=True, max_length=1900) 
    image = models.ImageField(upload_to = "service/images",default = "")
    price =models.IntegerField(default=0)
    Categorie =models.ForeignKey(Categorie,on_delete=models.CASCADE,default=1)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name =models.CharField(max_length=50)
    email =models.CharField(max_length=70,default="")
    phone =models.CharField(max_length=70,default="")
    desc =models.CharField(max_length=500,default="")
    def __str__(self):
            return self.name






class User(AbstractUser):
    # id= models.UUIDField(primary_key= True,default=uuid.uuid4, editable=False) 
    username = None
    email = models.EmailField(unique=True)
    is_verified =models.BooleanField(default=False)
    last_login_time = models.DateTimeField(null=True,blank=True)
    last_logout_time = models.DateTimeField(null=True,blank=True)

    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)

class CartService(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + "CartService: " + str(self.id)
ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On The Way", "On The Way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled")
)
# METHOD = (
#     ("Cash On Delivery ", "Cash On Delivery "),
# )
# SERVICE_MODE=(
#     ("Self Pick up and Drop","Self Pick up and Drop"),
#     (" Pick up and Drop by Mechanic","Pick up and Drop by Mechanic"),

# )


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    address = models.CharField(max_length=200 ,default="")
    date =models.DateField(null=True,blank=True)
    Time =models.TimeField(null=True,blank=True)
    mobile = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    # type =models.CharField(max_length=50,choices=SERVICE_MODE ,default="" )


    def __str__(self):
        return "Order: " + str(self.id)







    



    










# Create your models here.
