from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, likeview,PostLikeList
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('like/<int:pk>/', views.likeview, name='likes'),
    # path('post/<int:pk>/postlikes/', views.post_likes, name='post-likes'),
    path('post/<int:pk>/postlikes/', PostLikeList.as_view(), name='post-likes'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
