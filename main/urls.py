from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path('dreams/', views.dreams, name='dreams'),
    path('dreams/<uuid:dream_id>/', views.dreams, name='specific_dream'),
]