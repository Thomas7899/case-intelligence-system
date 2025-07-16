from django.urls import path
from . import views

app_name = 'investigations'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('cases/', views.case_list, name='case_list'),
    path('cases/<int:case_id>/', views.case_detail, name='case_detail'),
    path('cases/create/', views.case_create, name='case_create'),
    path('cases/<int:case_id>/edit/', views.case_edit, name='case_edit'),
    path('cases/<int:case_id>/delete/', views.case_delete, name='case_delete'),
    path('cases/<int:case_id>/timeline/add/', views.timeline_add, name='timeline_add'),
    path('timeline/<int:timeline_id>/edit/', views.timeline_edit, name='timeline_edit'),
    path('timeline/<int:timeline_id>/delete/', views.timeline_delete, name='timeline_delete'),
    path('search/', views.search, name='search'),
]
