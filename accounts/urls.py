from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

# namespace가 accounts라는 이름을 가졌음을 명시
app_name = "accounts"

urlpatterns = [
    path('temp/', views.temp, name='temp'), # 임시 홈
    path('signup/', views.signup, name='signup'), # 회원가입 
    path('login/', views.login, name='login'), # 로그인
    path('logout/', views.logout, name='logout'), # 로그아웃
    path('logoutTemp/', views.logoutTemp, name='logoutTemp'),  # '로그아웃 후 확인 페이지
    
    path('check_email/', views.check_email, name='check_email'),  # 이메일 인증(중복으로 기능 대체)

    path('find_id/', views.find_id, name='find_id'),  # 아이디 찾기
    path('verify_email/', views.verify_email, name='verify_email'),  # 아이디 찾기 시 이메일 인증

    path('reset_password/', views.reset_password, name='reset_password'),  # 비밀번호 재설정 페이지
    path('reset_password_confirm/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),  # 비밀번호 재설정 하는 페이지
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),  # 비밀번호 재설정 메일 보내기 완료
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),  # 비밀번호 재설정 완료

]