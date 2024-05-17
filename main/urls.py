from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path('dreams/', views.dreams, name='dreams'),
    path('consult/', views.consult, name='consult'),
    path('analyticalPsychology/', views.analyticalPsychology, name='analyticalPsychology'),
    path('animus/', views.animus, name='animus'),
    path('anima/', views.anima, name='anima'),
    path('typology/', views.typology, name='typology'),
    path("error/", views.error, name="error"),
    path('dreams/<uuid:dream_id>/', views.dreams, name='specific_dream'),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

