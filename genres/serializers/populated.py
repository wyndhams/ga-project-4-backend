from .common import GenreSerializer
from festivals.serializers.common import FestivalSerializer

class PopulatedGenreSerializer(GenreSerializer):
    festivals = FestivalSerializer(many=True)
