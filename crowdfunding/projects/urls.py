from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('projects/', views.ProjectList.as_view(), name="project-list"),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name='project-detail'),
    path('pledges/', views.PledgeList.as_view(), name="pledge-list"),
    path('pledges/<int:pk>/', views.PledgeDetailView.as_view(), name='pledge-detail'),
    path('comments/', views.CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>/', views.CommentDetail.as_view(), name='comment-detail'),
    path('search/', views.GlobalSearchList.as_view(), name="search"),
    
    # path('comments/<int:project_pk>/', views.CommentList.as_view(), name='comment-list'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
