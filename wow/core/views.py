from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, PostReply, Author
from .forms import PostForm, ReplyForm, NewsMailForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib.auth.models import User


def home(request):
    return render(request, 'index.html')


class PostList(ListView):
    """ Page with all posts sorted by date """
    model = Post
    ordering = '-publication_date'
    queryset = Post.objects.all()
    template_name = 'post_list.html'
    context_object_name = 'post_list'


def PostDetail(request, pk):
    """ Page with detailed view of one of the posts. Has a comment section """
    post_page = Post.objects.get(pk = pk)

    form = ReplyForm()
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            PostReply.objects.create(user=request.user, post=post_page, content=content)
            messages.success(request, (f"Отзыв был оставлен"))

        return HttpResponseRedirect(request.path_info)

    context = {
        'post_page': post_page,
        'form': form
    }
    return render(request, 'post_page.html', context)


class PostCreate(LoginRequiredMixin, CreateView):
    """ Form for creating a post. Only availavle to logged users """
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')

    # Filling up the Author field automatically
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.filter(user=self.request.user).first()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    """ Form for editing a post. Only availavle to creator of a post """
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')

    # making sure it's the owner of post, if not - they'll get 404
    def get_queryset(self):
        queryset = super(PostUpdate, self).get_queryset()
        queryset = queryset.filter(author__user=self.request.user)
        return queryset


class PostDelete(LoginRequiredMixin, DeleteView):
    """ Form for deleting a post. Only availavle to creator of a post """
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')

    # making sure it's the owner of post, if not - they'll get 404
    def get_queryset(self):
        queryset = super(PostDelete, self).get_queryset()
        queryset = queryset.filter(author__user=self.request.user)
        return queryset


class ProfileView(LoginRequiredMixin, ListView):
    """ Profile page """
    model = PostReply
    template_name = 'profile.html'
    context_object_name = 'reply_list'

    # Solution for sorting replies. By acceptance->date is default, by post title the alternative.
    def get_queryset(self):
        order_by = self.request.GET.get('order_by') or '-publication_date'
        return PostReply.objects.filter(post__author__user=self.request.user).order_by(order_by)


@login_required
def accept_reply(request, pk):
    """ A thing that triggers by pressing accept link on profile page """
    reply = PostReply.objects.get(pk=pk)

    # If the post owner clicked on it
    if reply.post.author.user == request.user:
        reply.accept()

        send_mail(
            subject=f"Ваш отклик был принят!",
            message=reply.post.author.user.username.capitalize() + f" пометил ваш отклик под объявлением " +
                    "*" + reply.post.title + "*. \n\n" + reply.content,
            from_email='biorival@yandex.ru',
            recipient_list=[reply.user.email],
            fail_silently=False,
        )

    return HttpResponseRedirect(reverse_lazy('profile'))


class ReplyDelete(LoginRequiredMixin, DeleteView):
    """ Form for deleting reply from profile page """
    model = PostReply
    template_name = 'reply_delete.html'
    success_url = reverse_lazy('profile')


def send_email_to_every_user(request):
    """ Newsletter. Form for sending email to every registered user. Available only for superusers """

    # The MEGASUPERDUPER protection
    if not request.user.is_superuser:
        messages.success(request, (f"Nice try, pal"))
        return HttpResponseRedirect(reverse_lazy('home'))

    form = NewsMailForm()
    if request.method == "POST":
        form = NewsMailForm(request.POST)
        if form.is_valid():
            users = User.objects.all()
            email_list = []
            for user in users:
                if user.email not in email_list:
                    email_list.append(user.email)

            send_mail(
                subject=form.cleaned_data['title'],
                message=form.cleaned_data['content'],
                from_email='biorival@yandex.ru',
                recipient_list=email_list,
                fail_silently=False,
            )

        return HttpResponseRedirect(request.path_info)
    else:
        return render(request, 'send_email_to_every_user.html', {'form':form})
