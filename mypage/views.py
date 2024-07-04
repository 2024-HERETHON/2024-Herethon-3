from django.shortcuts import render, redirect
from board.models import Post
from study.models import SubmitAnswer, SavedFlashCard
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404

# 마이 페이지
def my_page(request):
    return render(request, 'my_page.html')

# 내가 쓴 글
@login_required(login_url='accounts:login')
def my_post(request):
    post_list = Post.objects.filter(author=request.user).order_by('-create_date')
    return render(request, 'my_post.html', {'post_list':post_list})

# 내가 쓴 글 삭제
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('mypage:my_post')

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

# 퀴즈 기록 삭제
def quiz_delete(request, answer_id):
    answer = get_object_or_404(SubmitAnswer, pk=answer_id)
    answer.delete()
    return redirect('mypage:my_quiz')

# 플래시 기록
@login_required(login_url='accounts:login')
def my_flash(request):
    flash_list = SavedFlashCard.objects.filter(user=request.user)
    return render(request, 'my_flash.html', {'flash_list':flash_list})

# 플래시 기록 삭제
def flash_delete(request, flash_id):
    card = get_object_or_404(SavedFlashCard, pk=flash_id)
    card.delete()
    return redirect('mypage:my_flash')