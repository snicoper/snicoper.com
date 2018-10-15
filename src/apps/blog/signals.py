import os

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from utils.images import ImageResize

from .models import Tag


@receiver(post_save, sender=Tag)
def tag_post_save(sender, created, instance, **kwargs):
    """Redimensiona el thumbnail."""
    image_resize = ImageResize(instance.thumbnail.path)
    image_resize.resize(
        save_path=instance.thumbnail.path,
        width=400,
        height=400
    )


@receiver(pre_delete, sender=Tag)
def tag_pre_delete(sender, instance, using, **kwargs):
    """Elimina un thumbnail al eliminar un Tag."""
    image_path = instance.thumbnail.path
    if os.path.exists(image_path):
        os.remove(image_path)
