from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        """
        Devuelve la lista completa de usuarios simulados.
        """
        return Response(data_list, status=status.HTTP_200_OK)
    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)
    
class DemoRestApiItem(APIView):

    def get_item_by_id(self, item_id):
        """Busca un item por ID en la lista simulada"""
        for item in data_list:
            if item['id'] == item_id:
                return item
        return None
     
    def put(self, request, item_id):
        existing_item = self.get_item_by_id(item_id)  # CORREGIDO AQUÍ
        if not existing_item:
            return Response({"error": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if "name" not in data or "email" not in data:
            return Response({"error": "Faltan campos obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        existing_item.update({
            "name": data["name"],
            "email": data["email"],
            "is_active": data.get("is_active", True),
        })

        return Response({"message": "Elemento actualizado completamente."}, status=status.HTTP_200_OK)

    def patch(self, request, item_id):
        existing_item = self.get_item_by_id(item_id)  # CORREGIDO AQUÍ
        if not existing_item:
            return Response({"error": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        existing_item.update(data)

        return Response({"message": "Elemento actualizado parcialmente."}, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        existing_item = self.get_item_by_id(item_id)  # CORREGIDO AQUÍ
        if not existing_item:
            return Response({"error": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        existing_item["is_active"] = False

        return Response({"message": "Elemento eliminado lógicamente."}, status=status.HTTP_200_OK)
