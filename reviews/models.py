from django.db import models

class Review(models.Model):
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    festival = models.ForeignKey(
        "festivals.Festival",
        related_name="reviews",
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
      "jwt_auth.User",
      related_name="reviews",
      on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Review {self.id}"