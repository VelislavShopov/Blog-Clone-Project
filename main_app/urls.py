from django.urls import path

from main_app import views

app_name = 'main_app'

urlpatterns = [
    path('create/',views.PostCreateView.as_view(), name='create_post'),
    path('<int:pk>/drafts',views.DraftsListView.as_view(), name='drafts'),
    path('<int:pk>',views.PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/publish', views.publish_post, name='publish_post'),
    path('<int:pk>/edit', views.PostUpdateView.as_view(), name='update_post'),
]