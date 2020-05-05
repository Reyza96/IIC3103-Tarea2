from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from honestomiguel import views

urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('hamburguesa/',
         views.HamburguesasList.as_view(),
         name='hamburguesas-list'),
    path('hamburguesa/<pk>/',
         views.HamburguesaDetail.as_view(),
         name='hamburguesa-detail'),
    path('ingrediente/',
         views.IngredientesList.as_view(),
         name='ingredientes-list'),
    path('ingrediente/<pk>/',
         views.IngredienteDetail.as_view(),
         name='ingrediente-detail'),
    path('hamburguesa/<pkh>/ingrediente/<pki>',
         views.IngredientesEnHamburguesa,
         name='ingrediente-en-hamburguesa'),
])

