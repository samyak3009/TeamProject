
from .forms import UploadForm, CommentForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from .models import Comment, Post, Category, Comment
from django.contrib.auth.decorators import login_required


@login_required
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


def search_data(request):
    if request.method == "POST":
        data = request.POST["search"]  # MUMBAI
        # print(data)
        status = Post.objects.filter(title__icontains=data)
        # print(status)
        return render(request, "blog/searchData.html", {"postes": status})

    else:
        return render(request, 'blog/searchData.html', {})


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def CategoryView(request, cats):
    category_post = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'blog/categories.html', {'cats': cats.title().replace('-', ' '), 'category_post': category_post})


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        categories_list = Category.objects.all()
        context = super(PostListView, self).get_context_data(**kwargs)
        context['categories_list'] = categories_list
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        totallikes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.request.user.id):
            liked = True
        context["totallikes"] = totallikes
        context["liked"] = liked
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = UploadForm
    context_object_name = 'post'
    template_name = 'blog/post_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    # def success(req):
    #     return render(req, 'blog/post_detail.html')


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comments.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    #form_class = UploadForm
    fields = '__all__'
    context_object_name = 'cats'
    template_name = 'blog/addCategory_form.html'
    #success_message = 'Employee successful created'
    success_url = '/add_category/'


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'post_image']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
