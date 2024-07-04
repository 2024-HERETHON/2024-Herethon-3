from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('', views.my_page, name='my_page'),
    path('my-post/', views.my_post, name='my_post'),
    path('my-like/', views.my_like, name='my_like'),
    path('my-quiz', views.my_quiz, name='my_quiz'),
    path('my-flash', views.my_flash, name='my_flash'),
    # 작성한 글 삭제
    path('my-post/delete/<int:post_id>/', views.post_delete, name='post_delete'),
    # 퀴즈 기록 삭제
    path('my-quiz/delete/<int:answer_id>/', views.quiz_delete, name='quiz_delete'),
    # 플래시 기록 삭제
    path('my-flash/delete/<int:flash_id>/', views.flash_delete, name='flash_delete'),
]