from django.shortcuts import render, redirect

from django.db import models, IntegrityError
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.contrib.auth import authenticate

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class ItemListView(ListView):
    queryset = Item.objects.all()
    template_name = 'items.html'


class ItemDetailView(DetailView):
    queryset = Item.objects.all()
    template_name = 'item_detail.html'


class ItemCreateView(CreateView):
    model = Item
    fields = ['name', 'description']
    template_name = 'item_create.html'


class ItemUpdateView(UpdateView):
    model = Item
    fields = ['name', 'description']
    template_name = 'item_update.html'


class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'item_delete.html'
    success_url = reverse('items')


def main_menu(request):
    menu = []
    menu.append(('Items', reverse('items')))
    if request.user.is_authenticated:
        menu.append(('Logout', reverse('logout')))
    else:
        menu.append(('Login', reverse('login')))
    return render(request, 'main_menu.html', {'menu': menu})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('items')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')


def logout(request):
    logout(request)
    return redirect('items')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                login(request, user)
                return redirect('items')
            except IntegrityError:
                return render(request, 'register.html', {'error_message': 'The username or email is already taken.'})
        else:
            return render(request, 'register.html', {'error_message': 'The passwords do not match.'})
    else:
        return render(request, 'register.html')