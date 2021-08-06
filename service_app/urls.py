# from django.contrib import admin
from django.urls import path
from service_app import views
from django.conf import settings
from django.conf.urls.static import static

import service_app
app_name = 'service_app' 
urlpatterns = [
    path("", views.index, name="home"),
    path("<int:myid>",views.showservice,name="showservice"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("search",views.SearchView.as_view(),name="search"),
    path("services", views.services, name="services"),
    path("<slug:category_slug>",views.services,name="service_category"),
    path("showservice/<int:myid>",views.showservice,name="showservice"),
    path("addtocart/<int:ser_id>",views.AddToCartView.as_view(), name='services'),
    path('service_app/mycart/', views.MyCartView.as_view(), name='mycart'),
    path('managecart/<int:cs_id>/', views.ManageCartView.as_view(), name='managecart'),
    path('emptycart/', views.EmptyCartView.as_view(), name='emptycart'),
     path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('service_app/register/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
     path('service_app/login/', views.CustomerLoginView.as_view(), name='customerlogin'),
     path('service_app/logout/', views.CustomerLogoutView.as_view(), name='customerlogout'),
      path('service_app/profile/', views.CustomerProfileView.as_view(), name='customerprofile'),
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)