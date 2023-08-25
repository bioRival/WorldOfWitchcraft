from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import PostCreate, PostUpdate, PostDelete, PostList, PostDetail, ReplyDelete, accept_reply

urlpatterns = [
    path('list/', PostList.as_view(), name = 'post_list'),
    path('<int:pk>', PostDetail, name='post_page'),
    path('create/', PostCreate.as_view(), name = 'post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('reply/<int:pk>/delete/', ReplyDelete.as_view(), name='reply_delete'),
    path('reply/<int:pk>/accept/', accept_reply, name='accept_reply'),
]