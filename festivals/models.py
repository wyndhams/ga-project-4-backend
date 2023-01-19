from django.db import models

class Festival(models.Model): 
    name = models.CharField(max_length=100)
    cover_image = models.CharField(max_length=300)
    genres = models.ManyToManyField(
        'genres.Genre', related_name="festivals",  blank=True)
    artists = models.ForeignKey(
        'artists.Artist', related_name="festivals", on_delete=models.CASCADE)
    owner = models.ForeignKey(
      'jwt_auth.User',
      related_name="festivals",
      on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name}"