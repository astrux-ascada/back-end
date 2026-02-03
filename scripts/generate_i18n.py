# /scripts/generate_i18n.py
"""
Generador de archivos de traducción (i18n) a partir de las claves de ErrorMessages.
"""
import inspect
import json
import os
import sys
from collections import defaultdict

# Añadir el directorio raíz al path para poder importar 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.error_messages import ErrorMessages

def generate_i18n_json(output_path: str, lang: str = "es"):
    """
    Genera un archivo JSON para un idioma específico a partir de las claves de ErrorMessages.
    """
    print(f"🔍 Analizando claves de ErrorMessages para el idioma '{lang}'...")

    # Usar un defaultdict anidado para construir la estructura JSON
    def nested_dict():
        return defaultdict(nested_dict)

    i18n_dict = nested_dict()

    # Obtener todos los atributos de la clase ErrorMessages
    attributes = inspect.getmembers(ErrorMessages, lambda a: not(inspect.isroutine(a)))
    keys = [a for a in attributes if not(a[0].startswith('__'))]

    for key, value in keys:
        parts = value.split('.')
        current_level = i18n_dict
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                # Última parte, asignar un valor por defecto
                # Reemplazar underscores con espacios y capitalizar para un valor legible
                default_text = part.replace('_', ' ').capitalize()
                current_level[part] = f"[{lang}] {default_text}" # Placeholder con el idioma
            else:
                current_level = current_level[part]

    # Crear el directorio de salida si no existe
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Escribir el archivo JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(i18n_dict, f, ensure_ascii=False, indent=2)

    print(f"✅ Archivo de traducción generado exitosamente en: {output_path}")

if __name__ == "__main__":
    # Definir la ruta de salida en una nueva carpeta 'i18n' en la raíz del proyecto
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_file_path = os.path.join(project_root, "i18n", "es.json")
    
    generate_i18n_json(output_file_path, lang="es")

    # Ejemplo para generar otro idioma
    # output_file_path_en = os.path.join(project_root, "i18n", "en.json")
    # generate_i18n_json(output_file_path_en, lang="en")
