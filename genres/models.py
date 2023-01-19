from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.name}"
