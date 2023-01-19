from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers.populated import PopulatedGenreSerializer
from .serializers.common import GenreSerializer
from .models import Genre


class GenreListView(APIView):

    def get(self, _request):
        genres = Genre.objects.all()
        serialized_genres = GenreSerializer(genres, many=True)
        return Response(serialized_genres.data, status=status.HTTP_200_OK)


class GenreDetailView(APIView):
    def get(self, _request, pk):
        genre = Genre.objects.get(pk=pk)
        serialized_genre = PopulatedGenreSerializer(genre)
        return Response(serialized_genre.data, status=status.HTTP_200_OK)
