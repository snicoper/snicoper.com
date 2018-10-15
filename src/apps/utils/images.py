import os

from PIL import Image


class ImageResize(object):
    """Redimensar imagen."""

    def __init__(self, path):
        """Inicializa atributos.

        Args:
            path (str): Ruta absoluta de la imagen, con la imagen.

        Attributes:
            path (str): Ruta absoluta de la imagen, con la imagen.
            scale (bool): Con escala, default True.
            quality (int): Calidad de la imagen, default 70.
            optimize (bool): Optimización, default True.
            png2jpeg (bool): Convertir png a jpeg, default False.
        """
        self.path = path
        self.scale = True
        self.quality = 70
        self.optimize = True
        self.png2jpeg = False

        if not os.path.exists(self.path):
            dirname = os.path.dirname(self.path)
            image_name = os.path.basename(self.path)
            raise FileNotFoundError(
                'La imagen {} no se encuentra en {}'.format(image_name, dirname)
            )

    def resize(self, save_path, width, height, prefix=''):
        """Redimensiona una imagen.

        Si la imagen es menor a la requerida, no hará nada.
        Para aumentar la imagen, establecer scale = False
        y creara las dimensiones de width y height.

        Para la calidad, usar quality y optimize.

        Args:
            save_path (str): Ruta absoluta para guardar la imagen, con nombre y extensión.
            width (float|int): Ancho.
            height (float|int): Alto.
            prefix (str): Prefijo que se añadirá al thumbnail.
        """
        img = Image.open(self.path)
        if self.scale:
            img_width, img_height = float(img.size[0]), float(img.size[1])
            if img_width > img_height or img_width == img_height:
                width = width
                height = int(img_height * (width / img_width))
            else:
                height = height
                width = int(img_width * (height / img_height))
        img = img.resize((width, height), Image.ANTIALIAS)
        if self.png2jpeg:
            img = img.convert('RGBA')
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        if prefix:
            basename = '{}{}'.format(prefix, os.path.basename(save_path))
            dirname = os.path.dirname(save_path)
            save_path = os.path.join(dirname, basename)
        img.save(save_path, optimize=self.optimize, quality=self.quality)
        img.close()
