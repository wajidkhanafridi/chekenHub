from django.shortcuts import render,redirect
from django.views import View
from .models import Customer, Product, AddToRentHouse, OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#def home(request):
# return render(request, 'app/home.html')
class ProductView(View):
    def get(self, request):
        totalitem = 0
        hensandrooster = Product.objects.filter(category='M')
        welsumrooster = Product.objects.filter(category='L')
        whitehens = Product.objects.filter(category='FT')
        HenChick = Product.objects.filter(category='S')
        DesiHens = Product.objects.filter(category='TB')
        
        if request.user.is_authenticated:
            totalitem = len(AddToRentHouse.objects.filter(user=request.user))
        
        return render(request, 'app/home.html', {'hensandrooster': hensandrooster, 'welsumrooster': welsumrooster, 'whitehens': whitehens, 'HenChick': HenChick, 'DesiHens':  DesiHens, 'totalitem':totalitem})

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:

            item_already_in_cart = AddToRentHouse.objects.filter(Q(product=product.id)&Q(user=request.user)).exists()

        return render(request, 'app/productdetail.html', {'product': product,'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    AddToRentHouse(user=user , product=product).save()
    return redirect('/cart')
  
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = AddToRentHouse.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping_amount= 50.0
        total_amount = 0.0
        cart_product = [p for p in AddToRentHouse.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:

            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request,'app/addtocart.html',{'carts':cart, 'totalamount':totalamount , 'amount':amount})
        else:
            return render(request, 'app/emptycart.html')

                

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = AddToRentHouse.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount= 70.0
        
        cart_product = [p for p in AddToRentHouse.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            
        data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount + shipping_amount
               }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = AddToRentHouse.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount= 50.0
        
        cart_product = [p for p in AddToRentHouse.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            
        data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount + shipping_amount
               }
        return JsonResponse(data)

def remove_cart(request):

    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = AddToRentHouse.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount= 50.0
        
        cart_product = [p for p in AddToRentHouse.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            
        data = {
                
                'amount': amount,
                'totalamount': amount + shipping_amount
               }
        return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html' , {'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op })


def peshawarhouse(request, data=None):
    if data == None:
        peshawarhouse = Product.objects.filter(category='M')
    elif data == 'flock' or data == 'hens':
        peshawarhouse = Product.objects.filter(category='M').filter(brand=data)


    elif data == 'below':
        peshawarhouse = Product.objects.filter(
            category='M').filter(discounted_price__lt=400)

    elif data == 'above':
        peshawarhouse = Product.objects.filter(
            category='M').filter(discounted_price__gt=100)

    return render(request, 'app/peshawarhouse.html', {'peshawarhouse': peshawarhouse})

def lahorehouse(request, data=None):
    if data == None:
        lahorehouse = Product.objects.filter(category='L')
    elif data == 'Rooster' or data == 'hens':
        lahorehouse = Product.objects.filter(category='L').filter(brand=data)


    elif data == 'below':
        lahorehouse = Product.objects.filter(
            category='L').filter(discounted_price__lt=1100)

    elif data == 'above':
        lahorehouse = Product.objects.filter(
            category='L').filter(discounted_price__gt=100)

    return render(request, 'app/lahorehouse.html', {'lahorehouse': lahorehouse })

def shaheentown(request, data=None):
    if data == None:
        shaheentown = Product.objects.filter(category='FT')
    elif data == 'Voit' or data == 'Nike':
        shaheentown = Product.objects.filter(category='FT').filter(brand=data)
    return render(request, 'app/shaheentown.html', {'shaheentown': shaheentown})

def alhramtown(request, data=None):
    if data == None:
        alhramtown = Product.objects.filter(category='TB')
    elif data == 'dh' or data == 'dh':
        alhramtown = Product.objects.filter(category='TB').filter(brand=data)
    return render(request, 'app/alhramtown.html', {'alhramtown': alhramtown})

def khyberkali(request, data=None):
    if data == None:
        khyberkali = Product.objects.filter(category='S')
    elif data == 'hc' or data == 'hc':
        khyberkali = Product.objects.filter(category='S').filter(brand=data)
    return render(request, 'app/khyberkali.html', {'khyberkali': khyberkali})

def search(request):
    q=request.GET['q']
    data = Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request, 'app/search.html', {'data': data})
    

#def customerregistration(request):
# return render(request, 'app/customerregistration.html')


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = AddToRentHouse.objects.filter(user=user)
    amount = 0.0
    shipping_amount= 70.0
    totalamount = 0.0
    cart_product = [p for p in AddToRentHouse.objects.all() if p.user == request.user] 
    if cart_product:

        for p in cart_product:

            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add':add , 'totalamount':totalamount , 'cart_items':cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = AddToRentHouse.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self , request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():

            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulation!! Profile Update Successfully')
        return render(request , 'app/profile.html', {'form':form ,'active':'btn-primary'})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

       

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})

