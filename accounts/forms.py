from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm as AuthPasswordResetForm, SetPasswordForm as AuthSetPasswordForm
from .models import CustomUsers
from django.core.exceptions import ValidationError

""" 회원가입 """
class SignupForm(UserCreationForm):
    userId = forms.CharField(max_length=15, label='아이디', required=True, widget=forms.TextInput(attrs={'placeholder': '아이디 입력'}))
    userEmail = forms.EmailField(label='이메일', required=True, widget=forms.EmailInput(attrs={'placeholder': '이메일 입력', 'style': 'width: 267px;'}))
    nickname = forms.CharField(max_length=15, label='닉네임', required=True, widget=forms.TextInput(attrs={'placeholder': '닉네임 입력'}))
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 입력'}))
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 확인'}))

    class Meta:
        model = CustomUsers
        fields = ['userId', 'userEmail', 'password1', 'password2', 'nickname']

    # 중복 아이디 
    def clean_userId(self):
        userId = self.cleaned_data.get('userId')
        if CustomUsers.objects.filter(username=userId).exists():
            raise forms.ValidationError('이미 사용 중인 아이디입니다.')
        return userId
    
    # 중복 이메일 (이메일 인증 기능 대체)
    def clean_userEmail(self):
        userEmail = self.cleaned_data.get('userEmail')
        if CustomUsers.objects.filter(email=userEmail).exists():
            raise forms.ValidationError('이미 사용 중인 이메일입니다.')
        return userEmail

    # 비밀번호 6자 제한
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError('비밀번호는 최소 6자 이상이어야 합니다.')
        return password1

    # 비밀번호 확인 로직
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return password2
    
    # 닉네임 중복 
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if CustomUsers.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError('이미 사용 중인 닉네임입니다.')
        return nickname

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.username = self.cleaned_data['userId']
        user.email = self.cleaned_data['userEmail']
        if commit:
            user.save()
        return user
    

""" 비밀번호 재설정 """
class CustomPasswordResetForm(AuthPasswordResetForm):
    email = forms.EmailField(label=False, max_length=254,widget=forms.EmailInput(attrs={'placeholder': '이메일 입력', 'class': 'form-control'})
    )
    

class CustomSetPasswordForm(AuthSetPasswordForm):
    new_password1 = forms.CharField(label="False", widget=forms.PasswordInput(attrs={'placeholder': '새 비밀번호 입력'}))
    new_password2 = forms.CharField(label="False", widget=forms.PasswordInput(attrs={'placeholder': '새 비밀번호 확인'}))

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        if len(new_password1) < 6:
            raise ValidationError('비밀번호는 최소 6자 이상이어야 합니다.')
        return new_password1

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError('비밀번호가 일치하지 않습니다.')
        return new_password2
    