import json
from todo.forms import *
from todo.taskform import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from todo.models import task,PRIORITY_CHOICES,STATUS_CHOICES
from todo.utils import get_list_from_set, get_data_dict

def auth_login(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/home')
    return HttpResponseRedirect(request.path_info+'?auth_error=true')


def user_logout(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseBadRequest()
    return HttpResponseBadRequest('Not Allowed')
 
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )
def register_success(request):
    return render_to_response(
    'registration/success.html',
)
    
@login_required
def home(request):
    task_data= task.objects.filter(user_name_id=request.user.id)
    return render_to_response(
    'home.html',
    { 'user': request.user ,'task_data':task_data}
    )

@csrf_exempt
@login_required
def add_task(request):
    status = get_list_from_set(STATUS_CHOICES)
    priority_types = get_list_from_set(PRIORITY_CHOICES)
    if request.method == 'POST':
        fields = ['title', 'description', 'priority', 'due_date']
        task_dict = get_data_dict(request, fields)
        task_dict['user_name'] = request.user   
        data = save_task(task_dict) 
        return HttpResponse(content=json.dumps(data),
                                content_type='application/json')    
    else:
     return render(request, 'addtask.html',\
                  {"STATUS_CHOICES": status,\
                   "PRIORITY_CHOICES": priority_types,\
                   })

def save_task(task_dict):
    try:
        task_obj = task(**task_dict)
        task_obj.save()
        message = 'Task successfully created'
    except Exception as ex:
        message = 'Some error occurred'
    return {'status': True, 'message': message}        



@csrf_exempt
@login_required
def edit_task(request, tid):
    status = get_list_from_set(STATUS_CHOICES)
    priority_types = get_list_from_set(PRIORITY_CHOICES)
    task_obj = get_task(tid, request.user)
    if request.method == 'POST':
        fields = ['title', 'description', 'priority', 'due_date','status']
        task_dict = get_data_dict(request, fields)  
        data = save_update_task(task_obj,task_dict) 
        return HttpResponse(content=json.dumps(data),
                                content_type='application/json')
    if task_obj:
        return render(request, 'edit_task.html',\
                  {"task": task_obj[0], "STATUS_CHOICES": status,\
                   "PRIORITY_CHOICES": priority_types,\
                   })
    else:
        return HttpResponseNotFound()   

def get_task(tid, user):
    return task.objects.filter(id=tid,user_name=user) 

def save_update_task(task, task_dict): 
    try:
        task.update(**task_dict)
        message = 'Task successfully updated'
    except Exception as ex:
        message = 'Some error occurred'
    return {'status': True, 'message': message}  

         