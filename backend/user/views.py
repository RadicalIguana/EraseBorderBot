from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.utils.translation import gettext_lazy as _

from .models import MyUser

import json
import re

@csrf_exempt
def get_user(request):
    """ Get user's data by chat_id """
    id = json.loads(request.body.decode('utf-8'))
    user_data = MyUser.objects.filter(chat_id=id['chat_id']).values()
    data = list(user_data)
    return JsonResponse({'data': data})

@csrf_exempt
def get_user_id(request):
    """ Check existing user """
    user_id = json.loads(request.body.decode('utf-8'))
    existing = MyUser.objects.filter(chat_id=user_id['data']).exists()
    return HttpResponse(existing)

@csrf_exempt
def create_user(request):
    user = MyUser()
    data = json.loads(request.body.decode('utf-8'))
    
    error = check_error(data)
    if len(error) != 0:
        return JsonResponse(error)
    
    user.chat_id = data["chat_id"]
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.phone = data["phone"]
    user.email = data["email"]
    user.save()
    return HttpResponse('OK')

def check_error(data):
    error = {}
    phone = MyUser.objects.filter(phone=data['phone']).exists()
    email = MyUser.objects.filter(email=data['email']).exists()
    
    phone_pattern = re.findall(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', data['phone'])
    if phone_pattern is not None:
        error['phone_error'] = 'Wrong phone number format'

    email_pattern = re.findall(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data['email'])
    if email_pattern is not None:
        error['email_error'] = 'Wrong email format'
    
    if phone:
        error['phone_error'] = 'Phone is existing'
    if email:
        error['email_error'] = 'Email is existing'
        
    if len(data['email']) == 0:
        error['email_error'] = 'Field must not be empty'
    if len(data['phone']) == 0:
        error['phone_error'] = 'Field must not be empty'
        
    if len(data['first_name']) == 0:
        error['first_name_error'] = 'Field must not be empty'
    if len(data['last_name']) == 0:
        error['last_name_error'] = 'Field must not be empty'
        
    return error