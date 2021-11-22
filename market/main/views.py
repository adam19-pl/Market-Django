from django.shortcuts import render, HttpResponse, redirect
from main.models import Item
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
def homepage(request):
    return render(request,template_name='main/home.html')

def itemspage(request):
    if request.method =='GET':
        items = Item.objects.filter(owner=None)
        return render(request, template_name="main/items.html", context={'items' : items})
    if request.method == 'POST':
        purchased_item = request.POST.get('purchased-item')
        if purchased_item:
            purchased_item_object = Item.objects.get(id=purchased_item)
            purchased_item_object.owner = request.user
            purchased_item_object.save()
            messages.success(request,f'Congratulations ! You bought {purchased_item} for {purchased_item_object.price} $')

        return redirect('items')


def loginpage(request):
    if request.method =='GET':
        return render(request, template_name='main/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f'Pomyślnie zalogowałeś się jako {user.username}')
            return redirect('items')

        else:
            messages.error(request,'Login lub hasło są nieprawidłowe ! ')
            return redirect('login')


def registerpage(request):
    if request.method =='GET':
        return render(request,template_name='main/register.html')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            login(request, user)
            messages.success(request,f'Pomyślnie zarejestrowałeś konto ! Jesteś zalogowany jako {user.username} ! ')
            return redirect('home')
        else:
            messages.error(request,f'Utworzenie konta nie powiodło się ... {form.errors}')
            return redirect('register')

def logoutpage(request):
    logout(request)
    messages.success(request,'Wylogowałeś się ze strony')
    return redirect('home')

def alluseritemspage(request):
    if request.method =='GET':
        items = Item.objects.filter(owner = request.user.id)
        return render(request, template_name='main/alluseritems.html', context={'items': items })

    if request.method =='POST':
        delete_item = request.POST.get('delete-item')
        if delete_item:
            delete_item_object = Item.objects.get(name=delete_item)
            delete_item_object.owner = None
            delete_item_object.save()
            messages.info(request,f'Usunałeś {delete_item_object.name} z Twoich rzeczy ! ')

        return redirect('alluseritems')
