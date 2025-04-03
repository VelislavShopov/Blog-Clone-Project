from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.api import success
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, CreateView, DetailView, UpdateView, DeleteView

from main_app.forms import PostForm
from main_app.models import *

# Create your views here.


class HomePageView(View):
    template_name = 'main_app/index.html'
    def get(self, request):
        context = dict()
        context['posts'] = Post.objects.filter(is_published=True)
        context['user'] = request.user
        return render(request,self.template_name, context)

class LoginFormView(FormView):
    template_name = 'main_app/login.html'
    form_class = AuthenticationForm
    success_url = '/'
    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.success_url)


class LogOutView(View):
    def get(self,request):
        logout(request)
        return redirect('/')

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'main_app/post_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DraftsListView(ListView):
    model = Post
    context_object_name = 'drafts'
    template_name = 'main_app/drafts.html'
    def get_queryset(self):
        return Post.objects.filter(is_published=False, author=self.request.user)


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['comments'] = Comment.objects.filter(post=self.get_object())
        return context

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'main_app/post_form.html'
    fields = ('title','content')

    def get_success_url(self):
        return reverse_lazy('main_app:post_detail',kwargs={'pk':self.object.pk})

class PostDeleteView(DeleteView):
    model=Post
    success_url = reverse_lazy('index')

def publish_post(request,pk):
    post = Post.objects.get(pk=pk)
    post.is_published = True
    post.save()
    return redirect('main_app:post_detail', pk=post.pk)


class CommentOnPostCreateView(CreateView):
    model = Comment
    fields= ('content',)
    success_url = '/'
    template_name = 'main_app/add_comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['post_pk'])
        form.save()
        return redirect('main_app:post_detail', pk=self.kwargs['post_pk'])