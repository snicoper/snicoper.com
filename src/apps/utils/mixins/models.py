import inspect
import os

from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class ImageUpdateModel(models.Model):
    """Cuando el campo 'imagen' cambia o elimina la imagen, elimina
    la anterior del disco.

    El nombre del los campos ImageField se especifica en '_image_fields',
    que por defecto es ['image'].

    Attributes:
        _image_fields (list): Nombre del los campos imágenes, por defecto ['images'].
    """
    _image_fields = ['image']

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.id:
            module = inspect.getmodule(self)
            klass = getattr(module, self.__class__.__name__)
            instance = klass.objects.get(pk=self.id)

            for field in self._image_fields:
                old_image_field = getattr(instance, field)
                super().save(*args, **kwargs)
                if old_image_field and old_image_field.path:
                    new_image_field = getattr(self, field)
                    if not new_image_field or old_image_field.path != new_image_field.path:
                        if os.path.exists(old_image_field.path):
                            os.remove(old_image_field.path)
        else:
            super().save(*args, **kwargs)


class SlugFieldModel(models.Model):
    """Campo SlugField."""
    title = models.CharField(
        verbose_name=_('Titulo'),
        max_length=255,
        unique=True
    )
    slug = models.SlugField(
        help_text=_('Si se quiere auto-generar otro slug, dejarlo en blanco.'),
        max_length=255,
        unique=True,
        blank=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Genera el slug.

        Si el slug esta vacio, se auto-generara.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
