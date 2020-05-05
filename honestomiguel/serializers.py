from rest_framework import serializers
from honestomiguel.models import LANGUAGE_CHOICES, STYLE_CHOICES, Hamburguesa, Ingrediente


class IngredienteSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Ingrediente
        fields = ['url', 'id', 'nombre', 'descripcion']


class HamburguesaSerializer(serializers.HyperlinkedModelSerializer):
    ingredientes = {}

    class Meta:
        model = Hamburguesa
        fields = ['url', 'id', 'nombre', 'precio', 'descripcion', 'imagen', "ingredientes"]



