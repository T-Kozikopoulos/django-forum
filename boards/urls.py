from django.urls import path
from . import views
from .views import PostCreateView, TopicCreateView


urlpatterns = [
    path('', views.index, name='index'),
    path('board/<name>/', views.board, name='board'),
    path('topic/<name>/', views.thread, name='thread'),
    path("user/register/", views.register, name="register"),
    path("user/logout/", views.logout_request, name="logout"),
    path("user/login/", views.login_request, name="login"),
    path("post/new/", PostCreateView.as_view(), name='post_create'),
    path("thread/new/", TopicCreateView.as_view(), name='topic_create'),
]
