from django.db import models

try:
    from pgvector.django import VectorField  # type: ignore[import-not-found]
except ImportError:
    class VectorField(models.Field):
        def __init__(self, *args, **kwargs):
            kwargs.setdefault("editable", False)
            super().__init__(*args, **kwargs)

# Create your models here.
class ChatMessage(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}: {self.content[:20]}..."


class SimpleTextEmbedding(models.Model):
    text = models.TextField()
    embedding = VectorField(
        dimensions=768,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
