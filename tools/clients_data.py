# -*- coding: utf-8 -*-
"""Logotipos de clientes para el carrusel (Home y Resultados).
Solo logos: no se indica qué módulo usa cada marca.
Fuente: SynologyDrive/1RedBrand/imgs/logos_BW_2025.png (caja = x0, y0, x1, y1 en esa lámina;
o la ruta de un archivo propio en tools/logo_src/; un cuarto valor opcional fija el nivel de gris que se trata como fondo).
Solo se incluyen marcas autorizadas para publicarse. Para regenerar los PNG: python tools/make_logos.py"""

import os
SOURCE = os.path.expanduser("~/SynologyDrive/1RedBrand/imgs/logos_BW_2025.png")

CLIENTS = [
    ("fiesta-americana", "Fiesta Americana", (580, 28, 808, 144)),
    ("fiesta-inn", "Fiesta Inn", (872, 16, 1036, 160)),
    ("gamma", "Gamma Hoteles", (1092, 48, 1304, 136)),
    ("helvex", "Helvex", (320, 190, 584, 300)),
    ("upaep", "UPAEP", (600, 200, 828, 280)),
    ("city-express", "City Express by Marriott", (900, 180, 1180, 292)),
    ("mision", "Hoteles Misión", (1284, 176, 1536, 292)),
    ("mottoz", "Mottoz", (478, 316, 622, 458)),
    ("aheta", "AHETA", (1050, 302, 1274, 496)),
    ("ucpuebla", "UC Puebla", (1336, 320, 1532, 464)),
    ("macom", "Macom", (380, 528, 592, 672), 178),  # fondo texturizado: corte manual
    ("hotel-trueba", "Hotel Trueba", (920, 520, 1072, 692)),
    ("laudex", "Laudex", (1096, 532, 1296, 664)),
    ("zamora-live", "Zamora Live", (1368, 524, 1540, 692)),
    ("una", "Unión Nacional Avícola", "logo_src/una.png"),
    ("jp-hoteles", "JP Hoteles", "logo_src/jp-hoteles.png", 172),
]
