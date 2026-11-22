from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from TaskManager.models import *
from TaskManager.forms import *


def login_view(request):
    form_data = AuthenticationForm()
    if request.method == 'POST':
        form_data = AuthenticationForm(request, data=request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            if user:
                login(request, user)
                return redirect('dashboard_view')

    context = {
        'form_title': 'User Login Page',
        'form_btn': 'Login',
        'title': 'Login',
        'form_data': form_data
    }

    return render(request, 'master/base-form.html', context)


def register_view(request):
    form_data = RegistrationForm()
    if request.method == 'POST':
        form_data = RegistrationForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('login_view')

    context = {
        'form_title': 'User Registration Page',
        'form_btn': 'Register',
        'title': 'Register',
        'form_data': form_data
    }

    return render(request, 'master/base-form.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')


@login_required
def dashboard_view(request):
    today = timezone.localdate()
    tasks = Task.objects.filter(user=request.user)

    context = {
        'title': 'Dashboard',
        'total_task': tasks.count(),
        'pending_task': tasks.filter(status='Pending').count(),
        'completed_task': tasks.filter(status='Completed').count(),
        'overdue_task': tasks.filter(status='Pending', due_date__lt=today).count(),
    }
    return render(request, 'dashboard.html', context)


@login_required
def task_list(request):
    context = {
        'title': 'Task List',
        'today': timezone.localdate(),
        'tasks': Task.objects.filter(user=request.user).order_by('due_date')
    }
    return render(request, 'task-list.html', context)


@login_required
def add_task(request):
    form_data = TaskForm()
    if request.method == 'POST':
        form_data = TaskForm(request.POST)
        if form_data.is_valid():
            form_data = form_data.save(commit=False)
            form_data.user = request.user
            form_data.save()
            messages.success(request, 'Task added successfully')
            return redirect('task_list')

    context = {
        'form_title': 'Add Task',
        'form_btn': 'Add Task',
        'title': 'Add Task',
        'form_data': form_data
    }
    return render(request, 'master/base-form.html', context)


@login_required
def update_task(request, id):
    data = get_object_or_404(Task, id=id, user=request.user)

    form_data = TaskForm(instance=data)
    if request.method == 'POST':
        form_data = TaskForm(request.POST, instance=data)
        if form_data.is_valid():
            form_data = form_data.save(commit=False)
            form_data.user = request.user
            form_data.save()
            messages.success(request, 'Task updated successfully')
            return redirect('task_list')

    context = {
        'form_title': 'Update Task',
        'form_btn': 'Update Task',
        'title': 'Update Task',
        'form_data': form_data
    }
    return render(request, 'master/base-form.html', context)


@login_required
def delete_task(request, id):
    get_object_or_404(Task, id=id, user=request.user).delete()
    messages.success(request, 'Task deleted successfully')
    return redirect('task_list')


@login_required
def complete_task(request, id):
    data = get_object_or_404(Task, id=id, user=request.user)
    data.status = 'Completed'
    data.save()
    messages.success(request, 'Task marked as completed')
    return redirect('task_list')
