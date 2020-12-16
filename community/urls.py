from django.urls import path
from . import views


urlpatterns = [
    path('', views.community_list_create),
    path('<int:community_pk>/', views.community_detail_update_delete),
    path('<int:community_pk>/comments/', views.create_comment),
    path('comments/', views.comment_list),
    path('comments/<int:comment_pk>/', views.comment_detail_update_delete),
]