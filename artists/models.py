from django.db import models

class Artist(models.Model):
    name = models.TextField(max_length=30)
    # description = models.TextField(max_length=30)

    def __str__(self):
        return f"{self.name}"
