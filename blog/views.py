from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
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
        total_likes = data.total_likes()
        context["total_likes"] = total_likes
        context["post_is_liked"] = liked
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

# def like_post(request):
# # posts = get_object_or_404(Post, id=request.POST.get('post_id'))
#     posts = get_object_or_404(post, id=request.POST.get('post_id'))
#     is_liked = False
#     if posts.likes.filter(id=request.user.id).exists():
#         posts.likes.remove(request.user)
#         is_liked = False
#     else:
#         posts.likes.add(request.user)
#         is_liked = True

#     return render(request, 'blog/home.html')


def like_button(request):
    if request.method == 'POST':
        user = request.user
        id = request.POST.get('pk', None)
        article = get_object_or_404(Post, pk=id)

        if article.likes.filter(id=user.id).exists():
            article.likes.remove(user)
        else:
            article.likes.add(user)

    context = {'likes_count': article.total_likes}
    return HttpResponse(json.dumps(context), content_type='application/json')
# class BlogPostDetailView(DetailView):
#     model = Post
#     # template_name = MainApp/BlogPost_detail.html
#     # context_object_name = 'object'

#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)

#         likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
#         liked = False
#         if likes_connected.likes.filter(id=self.request.user.id).exists():
#             liked = True
#         data['number_of_likes'] = likes_connected.number_of_likes()
#         data['post_is_liked'] = liked
#         return data