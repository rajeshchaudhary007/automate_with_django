from django.shortcuts import render,redirect
from django.http import HttpResponse
from dataentry.tasks import celery_test_task
from .forms import RegistrationForm
from django.contrib import messages


from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth



def home(request):
    return render(request,'home.html')


def celery_test(request):
    celery_test_task.delay()
    return HttpResponse("<h3>Function executed successfully</h3>")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration successful.")
            return redirect('login')
    else:
        form = RegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request,'registration.html',context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST) 
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                login(request,user)
                messages.success(request,"Logged in successfully!")
                return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
        
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    messages.success(request,'Logout successfully!')
    return redirect('home')