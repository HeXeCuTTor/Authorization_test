from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.http import JsonResponse

from BACKEND.models import User, Invite, SendCode
from BACKEND.serializer import UserSerializer, UserNonInvitedSerializer
from info import SALT
from time import sleep
import random
import string

# Авторизация пользователя
class AuthUser(APIView):
    def post(self, request, *args, **kwargs):
        if {'phone', 'password'}.issubset(request.data):
            sleep(2)
            if {'invite_code'}.issubset(request.data):
                try:
                    invite = Invite.objects.get(code=request.data['invite_code']).user.id
                except Invite.DoesNotExist:
                    return JsonResponse({"Status": "Wrong invite code"})
                request.data['invited_by'] = invite
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                user.set_password(request.data['password']+SALT)
                user.save()
                user_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                Invite.objects.create(user_id=user.id, code=user_code)
                SendCode.objects.get_or_create(user_id=user.id) 
                return JsonResponse({'Status': True, 'Message': 'Check code was sending for your number'})
            else:
                user = User.objects.filter(phone=request.data['phone']).first()
                SendCode.objects.get_or_create(user_id=user.id)
                return JsonResponse({'Status': 'User has already created, check code on your number'})
        else:    
            return JsonResponse({'Status': False, 'Errors': 'Not all agruments'})

# Подтверждение(ввод данных с телефона)
class ConfirmAccountUser(APIView):
    def post(self, request, *args, **kwargs):
        if {'code'}.issubset(request.data):
            code = SendCode.objects.filter(key=request.data['code']).first()
            # print(token)
            if code is not None:
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': 'Wrong code'})
        else:
            return JsonResponse({'Status': False, 'Errors': 'Not all arguments'})

# Получение данных аккаунта
class DetailAccount(APIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.filter(phone=request.data['phone']).first()  
        if user.__dict__['invited_by'] is None:   
            serializer = UserNonInvitedSerializer(user)
        else:
            serializer = UserSerializer(user)
        return Response(serializer.data)

# Получение телефонов приглашенных аккаунтов   
class WhoUsedInvite(APIView):
    def get(self, request, *args, **kwargs):
        parent_user = User.objects.get(phone=request.data['phone'])
        user_id = parent_user.__dict__['id']
        invited_users = User.objects.filter(invited_by=user_id).all()
        users = UserSerializer(invited_users, many=True)
        phones = []
        for user in users.data:
            phones.append(user['phone'])
        return Response(phones)

