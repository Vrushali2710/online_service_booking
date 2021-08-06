from django.contrib import admin

# Register your models here.
from .models import *
models = (User,Vehicle,Model,Categorie,Service,Contact,Customer,Cart,CartService,Order)


admin.site.register(models)