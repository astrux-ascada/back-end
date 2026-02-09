# Módulo de Configuración

## 1. Visión General

El módulo de Configuración es el "panel de control" de Astruxa. Permite a los usuarios con el rol `SuperUser` modificar el comportamiento y las reglas de negocio de la aplicación en tiempo real, sin necesidad de realizar nuevos despliegues de código. Esto dota al sistema de una flexibilidad y adaptabilidad de nivel empresarial.

---

## 2. Arquitectura y Componentes

Este módulo gestiona dos tipos principales de configuración:

### 2.1. Parámetros de Configuración

-   **Modelo `ConfigurationParameter`**: Una tabla clave-valor que almacena parámetros globales del sistema.
    -   **Ejemplo:** La clave `procurement.ai.provider_suggestion_count` con el valor `3`.
-   **Funcionalidad**: Otros servicios pueden consultar estos parámetros para ajustar su comportamiento. Por ejemplo, el servicio de compras leería este parámetro para saber cuántos proveedores debe sugerir la IA.

### 2.2. Enums Dinámicos

-   **Modelos `EnumType` y `EnumValue`**: En lugar de tener listas de opciones "hardcodeadas" (como los estados de una orden de trabajo), este sistema las gestiona en la base de datos.
    -   **Ejemplo:** Un `EnumType` llamado `WorkOrderStatus` contiene `EnumValues` como `OPEN`, `IN_PROGRESS`, `COMPLETED`, etc.
-   **Funcionalidad**: Permite a un `SuperUser` añadir, eliminar o modificar las opciones disponibles en la aplicación (ej: añadir un nuevo estado "ESCALATED" a las órdenes de trabajo) a través de la API, y estos cambios se reflejan inmediatamente en la interfaz de usuario.

### 2.3. API (`/configuration`)

-   Expone una serie de endpoints protegidos exclusivamente para `SuperUsers` que permiten la gestión completa (CRUD) de los parámetros y los enums dinámicos.
