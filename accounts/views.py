from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import SignupForm, CustomPasswordResetForm, CustomSetPasswordForm
from .models import CustomUsers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 비밀번호 재설정 위한 세팅
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

# 임시페이지
def temp(request):
    return render(request, 'temp.html')

def logoutTemp(request):
    return render(request, 'logout.html')

""" 회원 가입 """
# 회원가입 시 이메일 인증  -> 이메일 중복으로 대체
@csrf_exempt  # 필요 시 CSRF 검사 비활성화
def check_email(request):
    email = request.POST.get('email')
    if CustomUsers.objects.filter(email=email).exists():
        return JsonResponse({'is_taken': True})
    else:
        return JsonResponse({'is_taken': False})

# 회원가입 
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})


""" 로그인/ 로그아웃 """
# 로그인 
def login(request):
    if request.method == 'POST':
        userId = request.POST['userId']
        password = request.POST['password']
        user = authenticate(request, username=userId, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('board:board')
        else:
            error_message = "아이디 또는 비밀번호가 잘못되었습니다."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

# 로그아웃
def logout(request):
    auth_logout(request)
    return redirect('mypage:my_page')


""" 아이디 찾기 """
# 아이디 찾기 용 이메일 확인
@csrf_exempt
def verify_email(request):
    email = request.POST.get('email')
    try:
        user = CustomUsers.objects.get(email=email)
        return JsonResponse({'exists': True, 'userId': user.username})
    except CustomUsers.DoesNotExist:
        return JsonResponse({'exists': False})
    

# 아이디 찾기
def find_id(request):
    return render(request, 'find_id.html')

""" 비밀번호 찾기 """
def reset_password(request):
    if request.method == 'POST':
        password_reset_form = CustomPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUsers.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',  # 또는 'https'
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                        print(f'Email sent to {user.email}')  # 디버그 메시지 추가
                    except Exception as e:
                        print(f'Error sending email: {e}')  # 예외 처리 및 오류 출력
            return redirect('accounts:password_reset_done')
    password_reset_form = CustomPasswordResetForm()
    return render(request, "password_reset.html", {"password_reset_form": password_reset_form})


def reset_password_confirm(request, uidb64=None, token=None):
    if request.method == 'POST':
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUsers.objects.get(pk=uid)
        set_password_form = CustomSetPasswordForm(user=user, data=request.POST)
        if set_password_form.is_valid():
            set_password_form.save()
            return redirect('accounts:password_reset_complete')  # 수정된 부분
    else:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUsers.objects.get(pk=uid)
        if user is not None and default_token_generator.check_token(user, token):
            set_password_form = CustomSetPasswordForm(user=user)
        else:
            set_password_form = None
    return render(request, "password_reset_confirm.html", {"set_password_form": set_password_form})

def password_reset_done(request):
    return render(request, 'password_reset_done.html')