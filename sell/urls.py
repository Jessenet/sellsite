from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='sell-home'),
    #path('', views.home, name='sell-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('item/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('item/new/', views.PostCreateView, name='post-create'),
    path('item/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('item/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='sell-about'),
]