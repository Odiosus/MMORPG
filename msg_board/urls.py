from django.urls import path
from django.views.generic import TemplateView

from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, ProfileListView, \
    PostFilterView, CommentListView, CommentCreateView, CommentDetail, confirm_comment, reject_comment, login_required

urlpatterns = [
    path('', PostListView.as_view(), name='posts'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('profile/', ProfileListView.as_view(), name='profile'),
    path('search/', PostFilterView.as_view(), name='search'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/', login_required(CommentListView.as_view()), name='comments'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment_detail'),
    path('comments/<int:pk>/confirm/', confirm_comment, name='confirm_comment'),
    path('comments/<int:pk>/reject/', reject_comment, name='reject_comment'),
    path('accept/', TemplateView.as_view(template_name='accept.html')),
    path('subscribe/', views.subscribe, name="subscribe"),

]
