import os

from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image

from config.settings.test import MEDIA_ROOT


def simple_uploaded_file(image_path):
    """Crea una SimpleUploadedFile para campos de modelo
    ImageField, FileField.

    Args:
        image_path (str): Path de la imagen a "subir".

    Returns:
        SimpleUploadedFile:
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError('El "{}" archivo no existe'.format(image_path))
    name = os.path.basename(image_path)
    with open(image_path, 'rb') as fh:
        image = SimpleUploadedFile(
            name=name,
            content=fh.read(),
            content_type='image/jpeg'
        )
    return image


def create_image(name='test.png', size=(150, 150), ext='png'):
    """Crea una imagen y la guarda en get_image_path.

    Args:
        name (str): Nombre de la imagen, por defecto test.png.
        size (list): width/height de la imagen, por defecto (150, 150).
        ext (str): Extension de la imagen sin el (.), por defecto png

    Returns:
        Imagen creada
    """
    color = (255, 0, 0, 0)
    image = Image.new('RGB', size=size, color=color)
    image.save(get_image_path(name), ext)
    return image


def get_image_path(name='test.png'):
    """Obtiene un path con la ruta y nombre de la imagen /MEDIA_ROOT/{name}.

    Args:
        name (str): Nombre de la imagen.

    Returns:
        El path con el nombre del archivo en forma de /MEDIA_ROOT/imagen.png
    """
    return '{}/{}'.format(MEDIA_ROOT, name)


def delete_image(name='test.png'):
    """Elimina una imagen.

    Args:
        name (str): Nombre de la imagen.
    """
    image_path = get_image_path(name)
    if os.path.exists(image_path):
        os.remove(image_path)
