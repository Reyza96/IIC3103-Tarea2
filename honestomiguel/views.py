from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from honestomiguel.models import Hamburguesa, Ingrediente
from honestomiguel.serializers import HamburguesaSerializer, IngredienteSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import Http404
from rest_framework.views import APIView


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'hamburgesas': reverse('hamburguesas-list', request=request, format=format),
        'ingredientes': reverse('ingredientes-list', request=request, format=format)
    })



class HamburguesasList(APIView):

    def get(self, request, format=None):
        hamburguesas = Hamburguesa.objects.all()
        serializer = HamburguesaSerializer(hamburguesas, many=True, context={'request': request})
        for j in serializer.data:
            for k in range(len((j['ingredientes']))):
                j['ingredientes'][k] = {'path': j['ingredientes'][k]}
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HamburguesaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientesList(APIView):

    def get(self, request, format=None):
        ingredientes = Ingrediente.objects.all()
        serializer = IngredienteSerializer(ingredientes, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = IngredienteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HamburguesaDetail(APIView):

    def get_object(self, pk):
        try:
            return Hamburguesa.objects.get(pk=pk)
        except Hamburguesa.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not pk.isnumeric():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        hamburguesa = self.get_object(pk)
        serializer = HamburguesaSerializer(hamburguesa, context={'request': request})
        i = serializer.data
        for k in range(len((i['ingredientes']))):
            i['ingredientes'][k] = {'path': i['ingredientes'][k]}
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        hamburguesa = self.get_object(pk)
        serializer = HamburguesaSerializer(hamburguesa, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            i = serializer.data
            for k in range(len((i['ingredientes']))):
                i['ingredientes'][k] = {'path': i['ingredientes'][k]}
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not pk.isnumeric():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        hamburguesa = self.get_object(pk)
        hamburguesa.delete()
        return HttpResponse(status=200)


class IngredienteDetail(APIView):

    def get_object(self, pk):
        try:
            return Ingrediente.objects.get(pk=pk)
        except Ingrediente.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not pk.isnumeric():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingrediente = self.get_object(pk)
        serializer = IngredienteSerializer(ingrediente, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        ingrediente = self.get_object(pk)
        serializer = IngredienteSerializer(ingrediente, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ingrediente = self.get_object(pk)
        if ingrediente.hamburguesa_set.all():
            return HttpResponse(status=409)
        else:
            ingrediente.delete()
            return HttpResponse(status=200)


@api_view(['PUT', 'DELETE'])
def IngredientesEnHamburguesa(request, pki, pkh):

    if not pki.isnumeric():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if not pkh.isnumeric():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        ingrediente = Ingrediente.objects.get(pk=pki)
    except Ingrediente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        hamburguesa = Hamburguesa.objects.get(pk=pkh)
    except Hamburguesa.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        hamburguesa.ingredientes.add(ingrediente)
        serializer = HamburguesaSerializer(hamburguesa, context={'request': request})
        i = serializer.data
        for k in range(len((i['ingredientes']))):
            i['ingredientes'][k] = {'path': i['ingredientes'][k]}
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        if hamburguesa.ingredientes.filter(id=pki):
            hamburguesa.ingredientes.remove(ingrediente)
            return Response(status=200)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
