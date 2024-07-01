from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Answer, Comment
from .forms import PostForm, AnswerForm, CommentForm, AreaForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, F, Value
from django.db.models.functions import Coalesce

def index(request):

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
    hot_posts = Post.objects.annotate(
        num=Coalesce(Count('answer'), Value(0)) + Coalesce(F('hits'), Value(0))
    ).order_by('-num', '-create_date')[:5]
    
    context = {'post_list' : post_list, 'so':so, 'hot_posts':hot_posts}
    return render(request, 'board/index.html', context)

# 전체 게시글 검색 기능
def post_search(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', '')
        post_list = Post.objects.filter(Q(subject__contains=searched) | Q(content__contains=searched))
        return render(request, 'board/index.html', {'post_list': post_list, 'searched': searched})
    else:
        return render(request, 'board/post_search.html')
    
# 지역 설정
def area_set(request):
    if request.method == 'GET':
        form = AreaForm()
        return render(request, 'board/area_set.html', {'form': AreaForm})
    else:
        form = AreaForm(request.POST)
        if form.is_valid():
            area1 = form.cleaned_data['area1']
            area2 = form.cleaned_data['area2']
            area3 = form.cleaned_data['area3']
            area = f"{area1} {area2} {area3}"
        return redirect('board:board_area', area = area)

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
    return render(request, 'board/post_area.html', context)

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
    return render(request, 'board/post_area.html', context)


# 지역별 게시글 생성
def post_create(request, area):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user
            post.create_date = timezone.now()
            post.area = area
            post.save()
            return redirect('board:board_area', area)
    else:
        form = PostForm()
    context = {'form':form}
    return render(request, 'board/post_form.html', context)

# 게시글 상세보기
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post':post}
    return render(request, 'board/post_detail.html', context)

# 답변 생성
def answer_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.post = post
            # answer.author = request.user.username
            answer.create_date = timezone.now()
            answer.save()
        return redirect('board:post_detail', post_id=post.id)
    else:
        form = AnswerForm()
    context = {'post': post, 'AnswerForm': form}
    return render(request, 'post_detail.html', context)

# 답변에 대한 댓글 생성
def comment_create(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.answer = answer
            comment.post = answer.post
            # comment.author = request.user
            comment.create_date = timezone.now()
            comment.save()
        return redirect('board:post_detail', post_id=answer.post.id)
    else:
        form = CommentForm()
    context = {'answer':answer, 'CommentForm':form}
    return render(request, 'post_detail.html', context)