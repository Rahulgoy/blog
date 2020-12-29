from django.shortcuts import render, get_object_or_404
from .models import Post, BlogComment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import NewCommentForm

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']         #to show most recent post
    paginate_by = 6
    
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     data = get_object_or_404(Post, id=self.kwargs['pk'])
    #     total_likes = data.total_likes()
    #     context["total_likes"] = total_likes
    #     return context
   
        
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']         #to show most recent post
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        data = get_object_or_404(Post, id=self.kwargs['pk'])
        liked=False
        if data.likes.filter(id=self.request.user.id).exists():
            liked=True
        comments_connected = BlogComment.objects.filter(blogpost_connected=self.get_object()).order_by('-date_posted')
        context['comments'] = comments_connected
        if self.request.user.is_authenticated:
            context['comment_form'] = NewCommentForm(instance=self.request.user)
        total_likes = data.total_likes()
        context["total_likes"] = total_likes
        context["post_is_liked"] = liked
        return context

    def post(self, request, *args, **kwargs):
        new_comment = BlogComment(content=request.POST.get('content'),
                                  author=self.request.user,
                                  blogpost_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)

class PostLikeList(DetailView):
    model = Post
    template_name = 'blog/post_likes.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = get_object_or_404(Post, id=self.kwargs['pk'])
        post_likes = posts.likes.all()
        context = {'post_likes': post_likes}
        return context







class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url = "/"
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def likeview(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))



# def post_likes(request, pk):
#     posts = get_object_or_404(Post, pk=pk)
#     post_likes = posts.likes.all()
#     data = Post.objects.all().filter(pk=pk)
#     context = {'post_likes': post_likes,
#                 'post': data,
#                 }
#     return render(request, 'blog/post_likes.html', context)