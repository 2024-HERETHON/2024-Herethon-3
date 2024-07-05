from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Answer, Comment, Info
from .forms import PostForm, AnswerForm, CommentForm, AreaForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, F, Value
from django.db.models.functions import Coalesce
from django.contrib import messages
def board(request):

    # 정렬 기준
    so = request.GET.get('so', 'recent')

    # 정렬
    if so == 'hit': # 조회순
        post_list = Post.objects.order_by('-hits', '-create_date')
    elif so == 'answer': # 댓글순
        post_list = Post.objects.annotate(
            num_answer = Count('answer')).order_by('-num_answer', '-create_date')
    else: # 최신순
        post_list = Post.objects.order_by('-create_date')

    # 인기 게시글
    # hot_posts = Post.objects.annotate(
    #     num=Coalesce(Count('answer'), Value(0)) + Coalesce(F('hits'), Value(0))
    # ).order_by('-num', '-create_date')[:5]

    hot_posts = Info.objects.order_by('-create_date')[:5]
    
    context = {'post_list' : post_list, 'so':so, 'hot_posts':hot_posts}
    return render(request, 'board.html', context)

# 정보 게시글 페이지
def info_detail(request, info_id):
    info = get_object_or_404(Info, pk=info_id)
    context = {'info':info}
    return render(request, 'info_detail.html', context)

# 전체 게시글 검색 기능
def post_search(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', '')
        post_list = Post.objects.filter(Q(subject__contains=searched) | Q(content__contains=searched))
        return render(request, 'board.html', {'post_list': post_list, 'searched': searched})
    else:
        return render(request, 'post_search.html')

def area_set(request):
    if request.method == 'GET':
        return render(request, 'area_set.html')
    else:
        si = request.POST.get('si')
        gu = request.POST.get('gu')
        dong = request.POST.get('dong')
        area = f"{si} {gu} {dong}"
    return redirect('board:board_area', area=area)

# 지역 게시판 보여주기
def board_area(request, area):
    areas = area.split()
    area3 = areas[2]

    # 정렬 기준
    so = request.GET.get('so', 'recent')

    post_list = Post.objects.filter(Q(area__contains=area)).order_by('-create_date')
    # 정렬
    if so == 'hit': # 조회순
        post_list = post_list.order_by('-hits', '-create_date')
    elif so == 'answer': # 댓글순
        post_list = post_list.annotate(
            num_answer = Count('answer')).order_by('-num_answer', '-create_date')
    else: # 최신순
        post_list = Post.objects.filter(Q(area__contains=area)).order_by('-create_date')

    # 인기 게시글
    hot_posts = post_list.annotate(
        num=Coalesce(Count('answer'), Value(0)) + Coalesce(F('hits'), Value(0))
    ).order_by('-num', '-create_date')[:5]

    context = {'area':area, 'area3':area3, 'post_list':post_list, 'hot_posts' : hot_posts, 'so':so,}
    return render(request, 'post_area.html', context)

# 지역 게시글 검색
def area_search(request, area):
    searched = request.POST.get('searched', '')
    areas = area.split()
    area3 = areas[2]
    # 설정된 지역 게시글 필터링
    post_list = Post.objects.filter(Q(area__contains=area))
    # 지역 게시글 중 검색어 필터링
    post_list = post_list.filter(Q(subject__contains=searched) | Q(content__contains=searched))
    context = {'area':area, 'area3':area3, 'post_list':post_list}
    return render(request, 'post_area.html', context)


# 지역별 게시글 생성
@login_required(login_url='accounts:login')
def post_create(request, area):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.area = area
            post.save()
            return redirect('board:board_area', area)
    else:
        form = PostForm()
    context = {'form':form}
    return render(request, 'post_form.html', context)

# 게시글 상세보기
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post':post}
    return render(request, 'post_detail.html', context)

# 답변 생성
@login_required(login_url='accounts:login')
def answer_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.post = post
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.save()
        return redirect('board:post_detail', post_id=post.id)
    else:
        form = AnswerForm()
    context = {'post': post, 'AnswerForm': form}
    return render(request, 'post_detail.html', context)

# 답변에 대한 댓글 생성
@login_required(login_url='accounts:login')
def comment_create(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.answer = answer
            comment.post = answer.post
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.save()
        return redirect('board:post_detail', post_id=answer.post.id)
    else:
        form = CommentForm()
    context = {'answer':answer, 'CommentForm':form}
    return render(request, 'post_detail.html', context)

# 게시글 좋아요
@login_required(login_url='accounts:login')
def vote_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        messages.error(request, "본인이 작성한 글은 추천할 수 없습니다")
    else: # 작성자 본인이 아님
        if post.voter.filter(pk=request.user.id).exists(): # 좋아요 취소
            post.voter.remove(request.user)
        else:
            post.voter.add(request.user) # 좋아요 추가
    return redirect('board:post_detail', post_id=post.id)

# 답변 좋아요
@login_required(login_url='accounts:login')
def vote_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author: # 작성자 본인 아님
        if answer.voter.filter(pk=request.user.id).exists(): # 좋아요 취소
            answer.voter.remove(request.user)
        else:
            answer.voter.add(request.user)
    return redirect('board:post_detail', post_id=answer.post.id)