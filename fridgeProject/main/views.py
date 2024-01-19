from django.shortcuts import render, redirect
from .forms import FridgeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Fridge
from django.shortcuts import get_object_or_404
from .forms import ProductManageForm
from .models import Product , FridgeProduct
from django.http import JsonResponse

def add_to_fridge(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        fridge_id = request.POST.get('fridge')
        fridge = Fridge.objects.get(id=fridge_id)
        product = Product.objects.get(id=product_id)

        print(fridge)
        print(product)
        print(quantity)
        # Check if the product is already in the fridge, update quantity if yes, else create a new entry
        fridge_product, created = FridgeProduct.objects.get_or_create(fridge=fridge, product=product)
        fridge_product.quantity = int(quantity)
        fridge_product.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

def modify_quantity(request, fridge_product_id):
    fridge_product = get_object_or_404(FridgeProduct, id=fridge_product_id)

    if request.method == 'POST':
        new_quantity = int(request.POST.get('new_quantity', 0))
        fridge_product.quantity = new_quantity
        fridge_product.save()

    # Redirect back to the fridge details page after modifying the quantity
    return redirect('main:fridge_details', fridge_id=fridge_product.fridge.id)

@login_required(login_url='main:login')
def home(request):
    user_fridges = Fridge.objects.filter(user=request.user)
    return render(request, 'main/home.html', {'user_fridges': user_fridges})

@login_required(login_url='main:login')
def create_fridge(request):
    if request.method == 'POST':
        form = FridgeForm(request.POST)
        if form.is_valid():
            fridge = form.save(commit=False)
            fridge.user = request.user  # Assign the current user to the fridge
            fridge.save()
            return redirect('main:home')  # Redirect to the home page or wherever you want
    else:
        form = FridgeForm()

    return render(request, 'main/create_fridge.html', {'form': form})

@login_required(login_url='main:login')
def fridge_details(request, fridge_id):
    # Retrieve the specific fridge or return a 404 error if not found
    user_fridge = get_object_or_404(Fridge, id=fridge_id, user=request.user)

    return render(request, 'main/fridge_details.html', {'user_fridge': user_fridge})


def products_manage(request):
    form = ProductManageForm()
    fridges = Fridge.objects.all()

    if request.method == 'POST':
        form = ProductManageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:products_manage')

    existing_products = Product.objects.all()
    categories = existing_products.values_list('category', flat=True).distinct()

    products_by_category = {}
    for category in categories:
        products_by_category[category] = existing_products.filter(category=category)

    context = {
        'form': form,
        'categories': categories,
        'products_by_category': products_by_category,
        'fridges': fridges,
    }

    return render(request, 'main/products_manage.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:home')
    else:
        form = AuthenticationForm()

    return render(request, 'main/login.html', {'form': form})
