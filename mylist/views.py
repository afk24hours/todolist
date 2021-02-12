from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.forms import modelform_factory

from .models import ToDoListObject, Category, Point
from .forms import ToDoForm, CategoryForm, PointForm, UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import *


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list')
        else:
            messages.error(request, 'Произошла ошибка при регистрации!')
    else:
        form = UserRegisterForm()
    return render(request, 'mylist/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list')
    else:
        form = UserLoginForm()
    return render(request, 'mylist/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


def index(request):
    if request.user.is_authenticated:
        list = ToDoListObject.objects.filter(created_by=request.user)
        if len(list)<1:
            return render(request, template_name='mylist/nothing.html')
        points = Point.objects.filter(created_by=request.user).prefetch_related('main')
        context = {
            'list': list,
            'points': points,
        }
        return render(request, template_name='mylist/todolistview.html', context=context)
    else:
        return render(request, template_name='mylist/todolistview.html')


class ToDoListByCategory(LoginRequiredMixin, ListView):
    model = ToDoListObject
    template_name = 'mylist/todolistview.html'
    context_object_name = 'todolist'
    allow_empty = True
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ViewDetails(LoginRequiredMixin, DetailView):
    model = ToDoListObject
    template_name = 'mylist/detail.html'
    context_object_name = 'list_detail'

    def get_queryset(self):
        return super(DetailView, self).get_queryset().filter(
            created_by=self.request.user
        )


class Search(LoginRequiredMixin, ListView):
    model = ToDoListObject
    template_name = 'mylist/todolistview.html'
    context_object_name = 'list'
    paginate_by = 12

    def get_queryset(self):
        return ToDoListObject.objects.filter(
            Q(title__icontains=self.request.GET.get('search')) & Q(created_by=self.request.user)
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = f"s={self.request.GET.get('search')}&"
        return context


@login_required(login_url='/login/')
def create_todolist(request):
    if request.method == 'POST':
        item = ToDoListObject(created_by=request.user)
        form = ToDoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/')
    else:
        form = ToDoForm()
        form.fields["category"].queryset = Category.objects.filter(created_by=request.user)
    return render(request, 'mylist/createtodolist.html', {'form': form})


@login_required(login_url='/login/')
def delete_todolist(request, pk):
    item = ToDoListObject.objects.get(pk=pk)
    if request.method == 'POST' and item.created_by == request.user:
        item.delete()
        return redirect('/')
    return render(request, 'mylist/deletetodolist.html', {'item': item})


@login_required(login_url='/login/')
def create_category(request):
    if request.method == 'POST':
        item = Category(created_by=request.user)
        form = CategoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/')
    else:
        form = CategoryForm()
    return render(request, 'mylist/createcategory.html', {'form': form})


def delete_point(request, pk):
    item = Point.objects.get(id=pk)
    if item.created_by == request.user:
        item = Point.objects.get(id=pk)
        item.delete()
    return redirect(f'/{item.main.id}')

def update_point(request, pk):
    item = Point.objects.get(id=pk)
    print(item.is_completed)
    if item.created_by == request.user:
        if item.is_completed == False:
            item.is_completed = True
            item.save()
        else:
            item.is_completed = False
            item.save()
    return redirect(f'/{item.main.id}')


def view_detail(request, pk):
    if ToDoListObject.objects.filter(pk=pk).exists():
        points = Point.objects.filter(main__id=pk)
        item = ToDoListObject.objects.get(pk=pk)
        if request.method == 'POST':
            form = PointForm(request.POST, use_required_attribute=False)
            if form.is_valid():
                data = form.cleaned_data['title']
                point = Point.objects.create(title=data, main=item, is_completed=False, created_by=request.user)
            return render(request, 'mylist/detail.html', {"list_detail": item, "form": form, "points": points})
        else:
            form = PointForm()
        if item.created_by == request.user:
            return render(request, 'mylist/detail.html', {"list_detail": item, "form": form, "points": points})
        else:
            return render(request, 'mylist/empty.html')
    else:
        return render(request, 'mylist/empty.html')
