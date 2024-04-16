from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# import razorpay 
from django.conf import settings
from .forms import ProductAddForm,UserAddForm,OrderPlaceForm




# --------------------------------------------------------- All Product Related Views -------------------------------------------------------------

class ProductView(View):
   def get(self,request):
      totalitems = 0
      topwears = Product.objects.filter(category='TW')
      bottomwears = Product.objects.filter(category='BW')
      mobiles = Product.objects.filter(category='M')
      if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
      return render(request,'app/home.html',{'topwears':topwears,'bottomwears': bottomwears,'mobiles':mobiles,'totalitems':totalitems})


class ProductDetailView(View):
  def get(self,request,pk):
    totalitems = 0
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    
    if request.user.is_authenticated:
      item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
      totalitems = len(Cart.objects.filter(user=request.user))

    return render(request,'app/productdetail.html',{'product':product,'item_al_in_cart':item_already_in_cart,'totalitems':totalitems})
  

@login_required
def mobile(request,data=None):
 totalitems = len(Cart.objects.filter(user=request.user))
 if data == None:
   mobiles = Product.objects.filter(category='M')
 elif data == 'Realmi' or data == 'Samsung' or data == 'OPPO' or data == 'OnePlus' or data == 'Apple' or data=='Vivo' or data=='Redmi':
   mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
   mobiles = Product.objects.filter(category='M',discount_price__lte=10000)
 elif data == 'above':
   mobiles = Product.objects.filter(category='M',discount_price__gte=10000)
 return render(request,'app/mobile.html',{'mobiles':mobiles,'totalitems':totalitems})

@login_required
def laptop_all(request,data=None):
  totalitems = len(Cart.objects.filter(user=request.user))
  if data == None:
    laptops = Product.objects.filter(category='L')
  elif data == 'Apple'  or data == 'Dell' or data == 'Lenovo' or data == 'VivoBook' or data=='HP':
    laptops = Product.objects.filter(category='L').filter(brand=data)
  elif data == 'below':
    laptops = Product.objects.filter(category='L',discount_price__lte=50000)
  elif data == 'above':
    laptops = Product.objects.filter(category='L',discount_price__gte=50000)
 
  return render(request, 'app/laptops.html',{'laptop':laptops,'totalitems':totalitems})
   
@login_required
def topwear_view(request):
  totalitems = len(Cart.objects.filter(user=request.user))
  topwear = Product.objects.filter(category='TW')
  return render(request,'app/topwear.html',{'topwear':topwear,'totalitems':totalitems})

@login_required
def bottomwear_view(request):
  totalitems = len(Cart.objects.filter(user=request.user))
  bottomwear = Product.objects.filter(category='BW')
  return render(request,'app/bottomwear.html',{'bottomwear':bottomwear,'totalitems':totalitems})




#---------------------------------------------------- Account Regitrstion View -----------------------------------------

class Registration(View):
  def get(self,request):
    form = CustomerRegistrationForm()

    return render(request,'app/customerregistration.html',{'form':form})
  
  def post(self,request):
    if request.method=='POST':
      fm = CustomerRegistrationForm(request.POST)
      if fm.is_valid():
        fm.save()
        messages.success(request,'Registration Successfully')
        # return HttpResponseRedirect('/login/')
    return render(request,'app/customerregistration.html',{'form':fm})
  



#---------------------------------------- Profile View -----------------------------------------------------------
  
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
  totalitems = 0
  def get(self,request):
    if request.user.is_superuser==True:
      return render(request,'app/admin.html')
    
    fm = CustomerProfileForm()
    totalitems = len(Cart.objects.filter(user=request.user))
    return render(request,'app/profile.html',{'form':fm,'active':'btn-primary','totalitems':totalitems})
  
  def post(self,request):
    form = CustomerProfileForm(request.POST)
    totalitems = len(Cart.objects.filter(user=request.user))
    if form.is_valid():
      user = request.user
      name = form.cleaned_data['name']
      mobile_number = form.cleaned_data['mobile_number']
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      state = form.cleaned_data['state']
      zipcode = form.cleaned_data['zipcode']
      reg = Customer(user=user,name=name,mobile_number=mobile_number,locality=locality,city=city,state=state,zipcode=zipcode)
      reg.save()
      messages.success(request,'Congratulation !! Profile has been Updated.')

    return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitems':totalitems})
    


# show customer data 
@login_required 
def address(request):
    totalitems = 0
    totalitems = len(Cart.objects.filter(user=request.user))
    add =  Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',{'add':add,'active':'btn-primary','totalitems':totalitems})



def update_adress(request,id):
  instance = Customer.objects.get(id=id)
  if request.method=='POST':
    fm = CustomerProfileForm(request.POST,instance=instance)
    if fm.is_valid():
      fm.save()
      
      return redirect('address')

  fm = CustomerProfileForm(instance=instance)
  return render(request,'app/update_address.html',{'form':fm})


def delete_adress(request,id):
  instance = Customer.objects.get(id=id)
  instance.delete()
  return redirect('address')




#----------------------------------------------------    Cart Related Views -------------------------------------------

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
  totalitems = 0 
  if request.user.is_authenticated:
   
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amout = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    totalitems = len(Cart.objects.filter(user=request.user))
    print(cart_product)  
    if cart_product:
      for p in cart_product:
        temp_amount = (p.quantity * p.product.discount_price)
        amount += temp_amount
        total_amount = amount + shipping_amount 

      return render(request,'app/addtocart.html',{'carts':cart,'amount':amount,'totalamount':total_amount,'totalitems':totalitems})
  return render(request,'app/emptycart.html')



@login_required
def plus_cart(request):
  if request.method=='GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity += 1
    c.save() 
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
      for p in cart_product:
        temp_amount = (p.quantity * p.product.discount_price)
        amount += temp_amount
     
      data = {
          'quantity':c.quantity,
          'amount':amount,
          'totalamount': amount + shipping_amount,
        }
      return JsonResponse(data)
      

@login_required
def minus_cart(request):
  if request.method=='GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity -= 1
    c.save() 
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
      for p in cart_product:
        temp_amount = (p.quantity * p.product.discount_price)
        amount += temp_amount
      
      data = {
          'quantity':c.quantity,
          'amount':amount,
          'totalamount': amount + shipping_amount,
        }
      return JsonResponse(data)



@login_required
def remove_cart(request):

  if request.method=='GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  
    c.delete() 
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    totalitems = len(Cart.objects.filter(user=request.user))
    if cart_product:
      for p in cart_product:
        temp_amount = (p.quantity * p.product.discount_price)
        amount += temp_amount
        
      data = {
         
          'amount':amount,
          'totalitems':totalitems,
          'totalamount': amount + shipping_amount,
        }
      return JsonResponse(data)
    




@login_required
def checkout(request):
 totalitems=0
 user = request.user
 adds = Customer.objects.filter(user=user)
 print(adds)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0 
 shipping_amount = 70.0
 total_amount = 0.0


#  razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_ID))
#  print(razorpay_client)

 cart_product = [p for p in Cart.objects.all() if p.user == user]
 totalitems = len(Cart.objects.filter(user=request.user))
 if cart_product:
   for p in cart_product:
    temp_amount = (p.quantity * p.product.discount_price)
    amount += temp_amount
   total_amount = amount + shipping_amount
   currency = 'INR'
   amount = total_amount * 100 

   
  #  razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
  #  print(razorpay_order)
  #  razorpay_order_id = razorpay_order['id']
   
   
 
 
 return render(request, 'app/checkout.html',{'add':adds,'totalamount':total_amount,'cart_item':cart_items,'totalitems':totalitems})



@login_required
def payment_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
    c.delete()
  return redirect('orders')




#------------------------------ Show All Orders --------------------------------------------

@login_required
def orders(request):
 totalitems = 0
 if request.user.is_authenticated:
   op = OrderPlaced.objects.filter(user=request.user)
   totalitems = len(Cart.objects.filter(user=request.user))

   return render(request, 'app/orders.html',{'order_placed':op,'totalitems':totalitems})







# ---------------------------------------- Admin Dashboard View -----------------------------------------------


@login_required
def view_product(request):
  products = Product.objects.all()
  return render(request,'app/view_products.html',{'products':products})


@login_required
def add_products(request):
  fm = ProductAddForm()
  if request.method=='POST':
    fm = ProductAddForm(request.POST,request.FILES)
    if fm.is_valid():
      fm.save()
      messages.success(request,'Product Added Successfully')
  return render(request,'app/add_products.html',{'form':fm})


@login_required
def update_products(request,id):
  product_instance = Product.objects.get(id=id)
  if request.method=='POST':
    form = ProductAddForm(request.POST,request.FILES,instance=product_instance)
    if form.is_valid():
      form.save()
      messages.success(request,'Product Updated Successfully !!')
    
    return render(request,'app/update_products.html',{'form':form})
  fm = ProductAddForm(instance=product_instance)
  return render(request,'app/update_products.html',{'form':fm})


@login_required
def delete_products(request,id):
  p_obj = Product.objects.get(id=id)
  p_obj.delete()
  return HttpResponseRedirect('/viewproducts/')

@login_required
def user_data(request):
  users = User.objects.all()
  return render(request,'app/users.html',{'users':users})

@login_required
def add_users(request):
  if request.method=='POST':
    form = UserAddForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'User created successfully !!')
      return render('users')

  form = UserAddForm()
  return render(request,'app/user_add.html',{'form':form})

@login_required
def update_user(request,id):
  user_instance = User.objects.get(id=id)
  if request.method=='POST':
    form = UserAddForm(request.POST,instance=user_instance)
    if form.is_valid():
      form.save()
      messages.success(request,'User Updated successfully !!')
      return render('users')
    
  form = UserAddForm(instance=user_instance)
  return render(request,'app/update_user.html',{'form':form})

@login_required
def delete_user(request,id):
  user_instance = User.objects.get(id=id)
  user_instance.delete()
  return redirect('users')

@login_required
def cart_data(request):
  carts = Cart.objects.all()
  return render(request,'app/cart_data.html',{'carts':carts})

      

def orders_data(request):
  op = OrderPlaced.objects.all()
  return render(request,'app/orders-data.html',{'op':op})




@login_required
def update_orders(request,id):
  user_instance = OrderPlaced.objects.get(id=id)
  if request.method=='POST':
    form = OrderPlaceForm(request.POST,instance=user_instance)
    if form.is_valid():
      form.save()
      messages.success(request,'Order Updated successfully !!')
      return redirect('orders-data')
    
  form = OrderPlaceForm(instance=user_instance)
  return render(request,'app/update_orders.html',{'form':form})


@login_required
def delete_orders(request,id):

  order_instance = OrderPlaced.objects.get(id=id)
  order_instance.delete()
  if request.user.is_superuser:
    return redirect('orders-data')
  else:
    return redirect('orders')
  



