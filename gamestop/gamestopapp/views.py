from django.shortcuts import render ,redirect,HttpResponse
from gamestopapp.models import product,cart,orders,review
from django.contrib.auth.models import User
from django.contrib.auth import login, logout ,authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection,EmailMessage
from django.conf import settings
import random
# Create your views here.
def index(request):
    return render(request,'index.html')

@login_required(login_url='/login')
def create_product(request):
    if request.method == 'GET':
        return render(request,'create_product.html')
    else:
        name = request.POST['name']
        description = request.POST['description']
        manufacturar =request.POST['manufacturar']
        category = request.POST['category']
        price = request.POST['price']
        image = request.FILES['image']
        p= product.objects.create(name=name,description=description,manufacturar=manufacturar,category=category,price=price,image=image)
        p.save()
        return redirect('/')
    


def user_register(request):
    if request.method == 'GET':
        return render(request,'register_pro.html')
    else:
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password= request.POST['confirm_password']
        if password == confirm_password:
            u = User.objects.create(username = username,first_name=first_name,last_name=last_name,email=email)
            u.set_password(password)
            u.save()
            return redirect('/')
        else:
            context ={"error":"password and confirm password doesnot match"}
            return render(request,'register_pro.html',context)
            

def read(request):
    
    if request.method == "GET":
        
        p = product.objects.all()
        context = {}
        context['data']=p
        return render(request,'read_product.html',context)
    else:
        name = request.POST['search']
        pro = product.objects.get(name = name)
        return redirect(f"product_detail/{pro.id}")

@login_required(login_url='/login')
def update(request, rid):
    if request.method == 'GET':
        
        p = product.objects.filter(id=rid)
        context = {}
        context['data'] = p
        return render(request,'update_product.html',context)
    else:
        name = request.POST['name']
        description = request.POST['description']
        manufacturar =request.POST['manufacturar']
        category = request.POST['category']
        price = request.POST['price']
        
        p= product.objects.filter(id = rid)
        p.update(name=name, description=description,manufacturar=manufacturar,category=category,price=price)
        return redirect('/read')
    
@login_required(login_url='/login')    
def delete_product(request,rid):
    p= product.objects.filter(id = rid)
    p.delete()
    
    return redirect('/read')
        
        
def user_login(request):
    if request.method == 'GET':
        return render(request, 'user_login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user= authenticate(username = username,password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {}
            context['error']= 'USERNAME and PASSWORD does not match'
            return render(request,'user_login.html',context)
        
        
def user_logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login')
def create_cart(request, rid):
    prod = product.objects.get(id=rid)
    cart_pro = cart.objects.filter(product=prod, user = request.user).exists()
    if cart_pro:
        return redirect('/read_cart')
    else:
        user = User.objects.get(username = request.user)
        total_price = prod.price
        c = cart.objects.create(product=prod,user = user ,quantity = 1,total_price= total_price)
        c.save()
        return redirect('/read_cart')


@login_required(login_url='/login')
def read_cart(request):
    c = cart.objects.filter(user = request.user)
    context ={'data': c}
    
    total_price = 0
    total_quantity = 0
    
    for i in c:
        total_price += i.total_price
        total_quantity += i.quantity
    context['total_price'] = total_price
    context['total_quantity'] = total_quantity
        
    return render(request,'read_cart.html',context)  

def delete_cart(request, rid):
    r_cart = cart.objects.filter(id = rid)
    r_cart.delete()
    return redirect('/read_cart')



def update_cart(request, rid, q):
    r_cart = cart.objects.filter(id = rid)
    c = cart.objects.get(id=rid)
    quantity = int(q)
    price = int(c.product.price) * quantity
    r_cart.update(total_price = price, quantity = q)
    return redirect('/read_cart')


def create_orders(request, rid):
    c = cart.objects.get(id=rid)
    o = orders.objects.create(product = c.product,user=request.user, quantity = c.quantity,total_price= c.total_price)
    o.save()
    c.delete()
    
    
    return redirect('/read_cart')



def read_orders(request):
    ord = orders.objects.filter(user = request.user)
    context = {}
    context['data']= ord
    return render(request, 'readorders.html', context)


def create_review(request, rid):
    prod = product.objects.get(id = rid)
    rev = review.objects.filter(user = request.user, product = prod).exists()
    if rev:
        return HttpResponse('Review Already Added')
    else:
        
        if request.method == 'GET':
            
            return render(request, 'createreview.html')
        else:
            title = request.POST['title']
            content = request.POST['content']
            rating = request.POST['rate']
            image = request.FILES['image']
            
            prod = product.objects.get(id = rid)
            rev = review.objects.create(product = prod , user = request.user, title = title, content = content,rating= rating, image = image)
            rev.save()
            
            return HttpResponse('Thanks For Your Valueable Review')
        
def read_product_details(request, rid):
    
    p =  product.objects.filter(id = rid)
    
    prod = product.objects.get(id = rid)
    
    
    
    n = review.objects.filter(product = prod).count()
    
    rev = review.objects.filter(product = prod)
    
    sum = 0
    for x in rev:
        sum += x.rating
    try:
        avg_r = sum/n
        avg = int(sum/n)
    except:
        print('No Review')
        
    context = {}
    context['data'] = p
    if n == 0:
        context['avg'] = 'No Review'
    else:
        context['avg_rating'] = avg
        context['avg'] = avg_r
    return render(request,'readproductdetail.html',context)



def forget_password(request):
    if request.method == "GET":
        
        return render(request,'forgotpassword.html')
    else:
        email = request.POST['email']
        request.session['email'] = email
        user = User.objects.filter(email = email).exists()
        if user:
            otp = random.randint(1000,9999)
            request.session['otp'] = otp
        
        
            with get_connection(
                host = settings.EMAIL_HOST,
                port = settings.EMAIL_PORT,
                username = settings.EMAIL_HOST_USER,
                password = settings.EMAIL_HOST_PASSWORD,
                use_tls = settings.EMAIL_USE_TLS
            ) as connection:
                
                subject = "OTP Verification"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                message = f"OTP is {otp}"
                
                EmailMessage(subject,message,email_from,recipient_list,connection=connection).send()
                
            return redirect('/otp_verify')
        else:
            context = {'error':'User Does Not Exist'}
    
            return render(request,'forgotpassword.html',context)
        
def otp_verify(request):
    if request.method == "GET": 
        return render(request,'otp.html')
    else:
        otp =int(request.POST['otp'])
        email_otp =int(request.session['otp'])
        
        if otp == email_otp:
            return redirect('/new_password')
        else:
            return HttpResponse('OTP Not Verified')
        
        
        
def new_password(request):
    if request.method == "GET":
        
        return render(request,'newpassword.html')
    else:
        email = request.session['email']
        
        new_password = request.POST['newpass']
        confirm_password = request.POST['confirmpass']
        
        user = User.objects.get(email = email)
        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            return redirect('/login')
        else:
            context = {'error':'Password And Confirm Password Does Not Match'}
            return render(request,'newpassword.html',context)