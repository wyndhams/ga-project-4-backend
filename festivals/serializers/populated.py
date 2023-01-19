from .common import FestivalSerializer
from genres.serializers.common import GenreSerializer
from artists.serializers.common import ArtistSerializer
from reviews.serializers.populated import PopulatedReviewSerializer

class PopulatedFestivalSerializer(FestivalSerializer):
    genres = GenreSerializer(many=True)
    artist = ArtistSerializer()
    reviews = PopulatedReviewSerializer(many=True)