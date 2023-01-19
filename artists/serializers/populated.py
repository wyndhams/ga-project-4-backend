from .common import ArtistSerializer
from festivals.serializers.common import FestivalSerializer

class PopulatedArtistSerializer(ArtistSerializer):
    festivals = FestivalSerializer(many=True)
