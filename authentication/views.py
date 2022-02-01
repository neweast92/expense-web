
from lib2to3.pgen2 import token
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from validate_email import validate_email
import json

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from authentication.utils import token_generator
from userpreferences.models import UserPreference

from django.urls import reverse
from django.contrib import auth


# Create your views here.
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        # Get user data
        # validate
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.error(request, '비밀번호는 8자 이상이여야 합니다.')
                    return render(request, 'authentication/register.html', context=context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False

                # path_to_view
                # - getting domain we are on
                # - relative url to verification
                # - encode uid
                # - token

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})
                activate_url = 'http://' + domain + link

                try:
                    email_subject = '계정생성 완료'
                    email_body = 'Hi ' + user.username + '\nPlease use this link to verify your account\n\n' + activate_url
                    email_msg = EmailMessage(
                        email_subject,
                        email_body,
                        'noreply@semycolon.com',
                        [email],
                    )
                    email_msg.send(fail_silently=False)
                except:
                    messages.error(request, '메일 발송에 실패하였습니다.')
                    
                user.save()
                messages.success(request, '계정이 생성되었습니다.')
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                messages.info(request,  '이미 활성화되었습니다.')
                return redirect('login')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()        
    
            messages.success(request, '계정이 활성되었습니다.')
            return redirect('login')    
        except Exception as ex:
            pass
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, '환영합니다, ' + user.username + '님')
                    return redirect('expenses')
                
                messages.error(request, '비활성화된 계정입니다. 메일을 확인하세요.')
                return render(request, 'authentication/login.html')
            
            messages.error(request, '이름과 암호를 정확히 입력해주세요.')
            return render(request, 'authentication/login.html')
        
        messages.error(request, '이름과 암호를 입력해주세요.')
        return render(request, 'authentication/login.html')
        

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, '로그아웃되었습니다.')
        return redirect('login')


class EmailValidationView(View):    
    def post(self, request):
        data=json.loads(request.body)
        email=data['email']

        if not validate_email(email):
            return JsonResponse({'email_error':'이메일이 유효하지 않습니다'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'동일한 이메일이 존재합니다'}, status=409)
        return JsonResponse({'email_valid':True})


class UsernameValidationView(View):    
    def post(self, request):
        data=json.loads(request.body)
        username=data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'이름은 영숫자로 구성되어야 합니다'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'동일한 이름이 존재합니다'}, status=409)
        return JsonResponse({'username_valid':True})