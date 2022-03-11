from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from .models import Post

class BlogListView( ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        # context['posts'] =  context['posts'].filter(author = self.request.user)
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['posts'] = context['posts'].filter(title__icontains=search_input)
        return context

class BlogDetailView(LoginRequiredMixin,DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_detail.html'

class BlogCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields =  ['title', 'body']
    template_name  = 'post_new.html'

    def get_success_url(self,**kwargs):
         return reverse('post_detail',kwargs={'pk':str(self.object.id)})
    
    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super(BlogCreateView,self).form_valid(form)
         
class BlogUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    fields =  ['title', 'body']
    template_name  = 'post_new.html'
    def get_success_url(self,**kwargs):
         return reverse('post_detail',kwargs={'pk':str(self.object.id)})

class BlogDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')

