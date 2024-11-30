from django.urls import path
from . import views

urlpatterns=[
    path('', views.presentation_list), # POST & GET
    path('login/', views.login), #GET
    path('join/<int:presentation_id>/', views.join_presentation), #POST
    path('slides/<int:presentation_id>/', views.presentation_slides), #GET
    path('edit_slide/<int:presentation_id>/<int:slide_id>/', views.edit_slide), #PUT
    path('manage_user/<int:presentation_id>/', views.manage_users), # GET, PUT
    path('presentation_mode/<int:presentation_id>/', views.presentation_mode) #GET
]