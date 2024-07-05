from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.board, name='board'),
    path('post/search/', views.post_search, name='post_search'),
    path('area/set/', views.area_set, name='area_set'),
    path('area/<str:area>', views.board_area, name='board_area'),
    path('area/search/<str:area>', views.area_search, name='area_search'),
    path('post/create/<str:area>', views.post_create, name='post_create'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('answer/create/<int:post_id>/', views.answer_create, name='answer_create'),
    path('comment/create/<int:answer_id>/', views.comment_create, name='comment_create'),
    path('info/<int:info_id>/', views.info_detail, name='info_detail'),
    # 좋아요 기능
    path('vote/post/<int:post_id>/', views.vote_post, name='vote_post'),
    path('vote/answer/<int:answer_id>/', views.vote_answer, name='vote_answer'),
]