from django.db import models


class AboutViews(models.Model):
    """Contador de paginas vistas en About.

    El modelo solo tiene una fila.
    """
    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        """Solo se permite tener una fila en el modelo."""
        if AboutViews.objects.count() > 0:
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.views)
