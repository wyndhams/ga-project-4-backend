from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.db import IntegrityError
from django.db.models import Q

from .models import Festival
from .serializers.common import FestivalSerializer
from .serializers.populated import PopulatedFestivalSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class FestivalListView(APIView):
    permission_classes = {IsAuthenticatedOrReadOnly, }

    def get(self, _request):
        festivals = Festival.objects.all()
        serialized_festivals = FestivalSerializer(festivals, many=True)
        return Response(serialized_festivals.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['owner'] = request.user.id
        print(request.data)
        festival_to_add = FestivalSerializer(data=request.data)
        try:
            festival_to_add.is_valid()
            festival_to_add.save()
            return Response(festival_to_add.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            res = {
                "detail": str(e)
            }
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({"detail": "Unprocessable Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class FestivalDetailView(APIView):
    permission_classes = {IsAuthenticatedOrReadOnly, }
    def get_festival(self, pk):
        try:
            return Festival.objects.get(pk=pk)
        except Festival.DoesNotExist:
            raise NotFound(detail="Can't find that festival!")

    def get(self, _request, pk):
        festival = self.get_festival(pk=pk)
        serialized_festival = PopulatedFestivalSerializer(festival)
        return Response(serialized_festival.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        festival_to_edit = self.get_festival(pk=pk)
        updated_festival = FestivalSerializer(festival_to_edit, data=request.data)
        try:
            updated_festival.is_valid()
            updated_festival.save()
            return Response(updated_festival.data, status=status.HTTP_202_ACCEPTED)
        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            res = {
                "detail": "Unprocessable Entity"
            }
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, _request, pk):
        print('DELETE ME')
        festival_to_delete = self.get_festival(pk=pk)
        festival_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FestivalSearch(APIView):
    def get(self, request):      
        query = request.GET.get('search')
        print(query)                
        results = Festival.objects.filter(Q(name__icontains=query) | Q(genres__icontains=query) | Q(artists__icontains=query))
        serialized_results = FestivalSerializer(results, many=True)
        return Response(serialized_results.data)