from django.conf import settings
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from django.core.exceptions import PermissionDenied

from .filters import SearchFilter
from .forms import CommentForm, AddPostForm
from .models import Post, Comment, SubscriberNews


class PostListView(ListView):
    model = Post
    template_name = 'msg_board/posts.html'
    context_object_name = 'posts'
    ordering = '-pub_date'
    paginate_by = 5
    extra_context = {
        'title': "Доска объявлений",
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'msg_board/post_detail.html'
    context_object_name = 'post_detail'
    queryset = Post.objects.all()


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'msg_board/post_create.html'
    title_page = 'Разместить объявление'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = AddPostForm
    login_url = '/accounts/login/'
    template_name = 'msg_board/post_edit.html'
    permission_required = ('msg_board.change_post',)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'msg_board/post_delete.html'
    success_url = reverse_lazy('posts')


class ProfileListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'msg_board/profile.html'


class PostFilterView(FilterView):
    model = Post
    ordering = '-pub_date'
    template_name = 'msg_board/search.html'
    context_object_name = 'search'
    filterset_class = SearchFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = SearchFilter(self.request.GET, queryset)
        return self.filterset.qs


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'msg_board/comments.html'
    context_object_name = 'comments'
    ordering = '-date_comment'  # TODO
    paginate_by = 5

    def get_queryset(self):
        queryset = Comment.objects.filter(post_comment__author=self.request.user)
        return queryset


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'msg_board/comment_create.html'
    form_class = CommentForm
    success_url = '/comments/'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = User.objects.get(id=self.request.user.id)
        comment.post_comment = Post.objects.get(id=self.kwargs['pk'])
        comment.save()
        result = super().form_valid(form)
        send_mail(
            subject=f'Новый комментарий к вашему объявлению: "{comment.post_comment.heading}"',
            message=f'Комментарий от {comment.author}: "{comment.text}".',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL]
        )
        return result


class CommentDetail(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = 'msg_board/comment_detail.html'
    context_object_name = 'comment_detail'

    def get_template_names(self):
        response = self.get_object()
        if response.post_comment.author == self.request.user:
            self.template_name = 'msg_board/comment_detail.html'
            return self.template_name
        else:
            raise PermissionDenied


@login_required()
def confirm_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.confirm = True
    comment.save()
    send_mail(
        subject=f'Принят комментарий от {comment.author}',
        message=f'Принят комментарий от {comment.author} к объявлению "{comment.post_comment.heading}"',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_FROM_EMAIL]
    )
    return render(request, 'msg_board/accept.html')


@login_required()
def reject_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.confirmation_comment = False
    comment.save()
    return HttpResponseRedirect(reverse('comments'))


# подписка на новости
@login_required
def subscribe(request):
    subscribe = SubscriberNews()
    subscribe.user = request.user
    subscribe.save()
    return redirect(request.META.get('HTTP_REFERER'))
