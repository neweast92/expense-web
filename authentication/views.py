from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
import json


# Create your views here.
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

class UsernameValidationView(View):    
    def post(self, request):
        data=json.loads(request.body)
        username=data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'이름은 영숫자로 구성되어야 합니다'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'동일한 이름이 존재합니다'}, status=409)
        return JsonResponse({'username_valid':True})

class UsernameValidationView(View):    
    def post(self, request):
        data=json.loads(request.body)
        username=data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'이름은 영숫자로 구성되어야 합니다'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'동일한 이름이 존재합니다'}, status=409)
        return JsonResponse({'username_valid':True})