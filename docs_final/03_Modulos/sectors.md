# Módulo de Sectores

## 1. Visión General

El módulo de Sectores proporciona la estructura organizativa para la planta. Un "Sector" representa un área física o lógica (ej: "Línea de Ensamblaje 1", "Área de Mantenimiento", "Calderas") donde se encuentran los activos y donde operan los usuarios.

Este módulo es clave para la contextualización de los datos y para la gestión de permisos y responsabilidades.

---

## 2. Arquitectura y Componentes

-   **Modelo `Sector`**: Una entidad simple que contiene un `name` y una `description`.

-   **Relaciones:** El modelo `Sector` está conectado a otras entidades clave a través de relaciones de muchos-a-muchos:
    -   **`users`**: Un sector puede tener muchos usuarios asignados, y un usuario puede estar asignado a múltiples sectores. Esto permite, por ejemplo, que un supervisor sea responsable de dos líneas de producción.
    -   **`assets`**: Un sector contiene múltiples activos. Esta relación nos permite organizar el inventario de la planta y filtrar los activos por su ubicación física o funcional.

-   **API (`/sectors`)**: Expone endpoints básicos para la gestión (CRUD) de los sectores, permitiendo a los administradores crear, listar, actualizar y eliminar las áreas de la planta.
