
from django.http import HttpResponse
from service_app.models import Vehicle,Categorie,Service,Contact,Cart,Customer,CartService,Order,User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView,View,CreateView,FormView
from django.urls import reverse_lazy
from .forms import CheckoutForm,CustomerRergistationForm,CustomerLoginForm

from django.shortcuts import HttpResponse, get_object_or_404, redirect,render

 
# Create your views here.

def index(request):
    
    # return HttpResponse("Hello, Cool IT Help!")
    return render(request,'index.html')

    
# def checkvehicle(request):
#     if request.method == 'POST':
#         chassis_no= Vehicle.objects.filter(chassis_no = request.POST['chassis_no']).exists()
#         if chassis_no == True:
#             vehicle = Vehicle.objects.filter(chassis_no = request.POST['chassis_no']).values()
#             context = {
#                 'vehicle' :vehicle,
#             }
#             return render(request,'service.html',context)
#         else:
#             messages.error(request, 'Enter Valid Chassis number.')
#             return render(request,'checkvehicle.html')
#     else:
#         return render(request,'checkvehicle.html')
        
  
    
    
class CustomerRegistrationView(SuccessMessageMixin,CreateView):
    template_name = 'customerregistration.html'
    form_class = CustomerRergistationForm
    success_url = reverse_lazy("service_app:home")
    success_message = "User has been Registered Sucessfully"

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        
        user = User.objects.create_user(email,password)
        form.instance.user = user
        login(self.request, user)
  
        return super().form_valid(form)
     
  

    # def get_success_url(self):
    #     if "next" in self.request.GET:
    #         next_url = self.request.GET.get("next")
    #         print(next_url)
    #         return next_url
    #     else:
    #         return self.success_url  
class CustomerLoginView(FormView):
    template_name = 'customerlogin.html'
    form_class = CustomerLoginForm
    success_url = reverse_lazy("service_app:home")

    #form_valid method is a type of post methd and is available in CreateView, FormView and UpdateView
    def form_valid(self, form):
        uem = form.cleaned_data.get("email")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uem, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form":self.form_class, "error":"Invalid Credentials"})
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url
class CustomerLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('service_app:home')

   


    
  
           
     

   
    
      
    

def about(request):
   
    return render(request,'about.html')
def checkout(request):
   
    return render(request,'checkout.html')


def services(request,category_slug=None):
    categorie =None
    categories =Categorie.objects.all()
    service =Service.objects.all()
    if category_slug:
        categorie =get_object_or_404(Categorie,slug=category_slug)
        service =service.filter(Categorie=categorie)
    return render(request,'services.html',{'categories':categories,'categorie':categorie,'service':service})
    
class SearchView(TemplateView):
    template_name ="search.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results =Service.objects.filter(name__contains=kw)
        context['results']=results
        
        return context
        



  

    
def showservice(request,myid):
    service =Service.objects.filter(id=myid)
    return render(request,'showservice.html',{'service':service[0]})
class AddToCartView(TemplateView):
    template_name = 'addtocart.html'
   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #get product id from requested url
        service_id = self.kwargs['ser_id']
   

    #     # get product
        service_obj = Service.objects.get(id=service_id)

    #     # check if cart exist
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            
            this_service_in_cart = cart_obj.cartservice_set.filter(service=service_obj)


    #         #Item already exist in cart
            if this_service_in_cart.exists():
                cartservice = this_service_in_cart.last()
                cartservice.quantity += 1
                cartservice.subtotal += service_obj.price
                cartservice.save()
                cart_obj.total += service_obj.price
                cart_obj.save()
               
    #         #Item does not exist in cart
            else:
                cartservice = CartService.objects.create(cart=cart_obj, service=service_obj,rate=service_obj.price, quantity=1, subtotal=service_obj.price)
                cart_obj.total += service_obj.price
                cart_obj.save()
               

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartservice = CartService.objects.create(cart=cart_obj, service=service_obj,rate=service_obj.price, quantity=1, subtotal=service_obj.price)
            cart_obj.total += service_obj.price
            cart_obj.save()
  
            

    #     # check product already exist in cart
     
        return context

        

class MyCartView(TemplateView):
    template_name = 'mycart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context
class ManageCartView(View):
    def get(self, request, *args, **kwargs):
        print("This is manage cart section")
        cs_id = self.kwargs["cs_id"]
        action = request.GET.get("action")
        cs_obj = CartService.objects.get(id=cs_id)
        cart_obj = cs_obj.cart

        if action == 'inc':
            cs_obj.quantity += 1
            cs_obj.subtotal += cs_obj.rate
            cs_obj.save()
            cart_obj.total += cs_obj.rate
            cart_obj.save()
        elif action == 'dcr':
            cs_obj.quantity -= 1
            cs_obj.subtotal -= cs_obj.rate
            cs_obj.save()
            cart_obj.total -= cs_obj.rate
            cart_obj.save()
            if cs_obj.quantity == 0:
                cs_obj.delete()
        elif action == 'rmv':
            cart_obj.total -= cs_obj.subtotal
            cart_obj.save()
            cs_obj.delete()
        else:
            pass
        
        return redirect('service_app:mycart')
class EmptyCartView(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartservice_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect('service_app:mycart')
class CheckoutView(SuccessMessageMixin, CreateView):
    template_name = 'checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy("service_app:home")

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated and request.user.customer:
    #         pass
    #     else:
    #         return redirect("/login/?next=/checkout/")
    #     return super().dispatch(request, *args, **kwargs)
    success_message = "your order has been placed"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id',None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "order Received"
            del self.request.session["cart_id"]
    
        else:
            return redirect("service_app:home")
        return super().form_valid(form)
class CustomerProfileView(TemplateView):
    template_name = 'customerprofile.html'

    def dispatch(self, request, *args, **kwargs):
        # if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
        if request.user.is_authenticated and request.user.customer:

            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer)
        context['orders'] = orders
        print(orders)
        return context




def contact(request):
    if request.method =="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        messages.success(request,"your message has been sent")
    return render(request,'contact.html')
 

