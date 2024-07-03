from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('', views.my_page, name='my_page'),
    path('my-post/', views.my_post, name='my_post'),
    path('my-like/', views.my_like, name='my_like'),
    path('my-quiz', views.my_quiz, name='my_quiz'),
]