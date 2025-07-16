from django.urls import path
from . import views

app_name = 'entities'

urlpatterns = [
    path('persons/', views.person_list, name='person_list'),
    path('persons/<int:person_id>/', views.person_detail, name='person_detail'),
    path('persons/create/', views.person_create, name='person_create'),
    path('addresses/', views.address_list, name='address_list'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('relationships/', views.relationship_graph, name='relationship_graph'),
    path('cross-case-analysis/', views.cross_case_analysis, name='cross_case_analysis'),
]
