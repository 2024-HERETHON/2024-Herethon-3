from django.shortcuts import render
from board.models import Post
from study.models import Quiz, SubmitAnswer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# 마이 페이지
def my_page(request):
    return render(request, 'my_page.html')

# 내가 쓴 글
@login_required(login_url='accounts:login')
def my_post(request):
    post_list = Post.objects.filter(author=request.user).order_by('-create_date')
    return render(request, 'my_post.html', {'post_list':post_list})

# 좋아요 한 글
@login_required(login_url='accounts:login')
def my_like(request):
    post_list = Post.objects.filter(voter=request.user).order_by('-create_date')
    return render(request, 'my_like.html', {'post_list':post_list})

# 퀴즈 기록
@login_required(login_url='accounts:login')
def my_quiz(request):
    answer_list = SubmitAnswer.objects.filter(user=request.user)
    return render(request, 'my_quiz.html', {'answer_list':answer_list})
