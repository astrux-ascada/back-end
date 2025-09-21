# /app/util/avatar_generator.py
import io
import logging
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# --- MEJORA: Añadir un logger específico para este módulo ---
logger = logging.getLogger("app.util.avatar_generator")

# --- MEJORA: Paleta de colores planos y agradables para los fondos ---
# Fuente: https://flatuicolors.com/
COLOR_PALETTE = [
    (26, 188, 156), (46, 204, 113), (52, 152, 219), (155, 89, 182),
    (52, 73, 94), (22, 160, 133), (39, 174, 96), (41, 128, 185),
    (142, 68, 173), (44, 62, 80), (241, 196, 15), (230, 126, 34),
    (231, 76, 60), (236, 240, 241), (149, 165, 166), (243, 156, 18),
    (211, 84, 0), (192, 57, 43), (189, 195, 199), (127, 140, 141),
]

# --- MEJORA: Definir la ruta base para encontrar los assets de forma segura ---
# Esto construye una ruta absoluta al directorio 'app', sin importar desde dónde se ejecute el script.
APP_DIR = Path(__file__).resolve().parent.parent


def get_initials(name: str) -> str:
    """Extrae las iniciales de un nombre completo."""
    if not name or not name.strip():
        return "??"
    parts = name.strip().upper().split()
    if len(parts) >= 2:
        return parts[0][0] + parts[-1][0]
    return parts[0][0]


def generate_default_icon(size: int = 200) -> bytes:
    """
    Genera un icono de silueta de usuario genérico y ligero.
    Esta función es un fallback robusto que no depende de archivos externos.
    """
    # Un color de fondo gris claro y neutro
    bg_color = (230, 230, 230)
    # Un color de silueta gris oscuro
    fg_color = (170, 170, 170)

    image = Image.new("RGB", (size, size), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Dibujar la cabeza (un círculo)
    head_radius = size * 0.25
    head_center_x = size / 2
    head_center_y = size * 0.35
    draw.ellipse(
        (
            (head_center_x - head_radius, head_center_y - head_radius),
            (head_center_x + head_radius, head_center_y + head_radius),
        ),
        fill=fg_color,
    )

    # Dibujar el cuerpo (un arco)
    draw.arc(
        (
            (size * 0.1, size * 0.6),
            (size * 0.9, size * 1.3),
        ),
        start=180,
        end=360,
        fill=fg_color,
        width=int(size * 0.15),
    )

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    return img_byte_arr.getvalue()


def generate_initials_avatar(
        initials: str, size: int = 200
) -> bytes:
    """
    Genera una imagen de avatar con iniciales.

    Args:
        initials: Las iniciales a mostrar (ej: "JD").
        size: El tamaño del avatar (ancho y alto en píxeles).

    Returns:
        Un objeto de bytes que representa la imagen PNG.
    """
    # Elige un color de fondo basado en un hash de las iniciales para que sea consistente
    bg_color = COLOR_PALETTE[hash(initials) % len(COLOR_PALETTE)]

    # Determina el color del texto (blanco o negro) para un buen contraste
    text_color = (255, 255, 255) if (bg_color[0] * 0.299 + bg_color[1] * 0.587 + bg_color[
        2] * 0.114) < 186 else (0, 0, 0)

    image = Image.new("RGB", (size, size), color=bg_color)
    draw = ImageDraw.Draw(image)

    font = None
    try:
        font_size = int(size * 0.5)
        # --- CORRECCIÓN DEFINITIVA: Usar la ruta absoluta al archivo de la fuente ---
        font_path = APP_DIR / "assets" / "fonts" / "Roboto-Bold.ttf"

        # --- MEJORA: Log para depuración ---
        logger.debug(f"Intentando cargar la fuente desde la ruta: {font_path}")

        font = ImageFont.truetype(str(font_path), font_size)
        logger.debug("Fuente personalizada cargada exitosamente.")


    except IOError:
        # --- MEJORA: Log de error detallado ---
        logger.error(
            f"ERROR CRÍTICO: No se pudo cargar la fuente desde '{font_path}'. "
            "Causas probables: 1) El archivo no existe en esa ruta. "
            "2) El entorno (ej. Docker) no tiene las librerías de FreeType instaladas para que Pillow pueda leer .ttf. "
            "Intentando usar la fuente por defecto."
        )
        try:
            font = ImageFont.load_default()
            logger.warning("Se está usando la fuente por defecto de Pillow. La apariencia puede variar.")
        except Exception as e:
            # --- MEJORA: Capturar el error del fallback ---
            logger.critical(
                "FALLO TOTAL: No se pudo cargar ni la fuente personalizada ni la fuente por defecto. "
                "El avatar no se puede generar. Error: %s", e, exc_info=True
            )
            # Devolvemos una imagen en blanco para no crashear el endpoint.
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="PNG")
            return img_byte_arr.getvalue()

    # Calcula la posición del texto para centrarlo
    if font:  # Solo dibujar si la fuente se cargó
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((size - text_width) / 2, (size - text_height) / 2 - size * 0.05)
        draw.text(position, initials, font=font, fill=text_color)

    # Guardar la imagen en un buffer de memoria
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    return img_byte_arr.getvalue()
