# Manual de Uso de la API - Astruxa Backend

Este documento proporciona una guía detallada sobre cómo utilizar los endpoints de la API de Astruxa. Se incluye información sobre las URLs, métodos HTTP, parámetros requeridos, esquemas de datos y ejemplos de uso.

## Tabla de Contenidos
1. [Dinámica de Roles y Permisos](#dinámica-de-roles-y-permisos)
2. [Visión del Modelo SaaS](#visión-del-modelo-saas)
3. [Visión de Arquitectura y Funcionamiento del Frontend](#visión-de-arquitectura-y-funcionamiento-del-frontend)
4. [Autenticación (Authentication)](#autenticación-authentication)
5. [Gestión SaaS (SaaS Management)](#gestión-saas-saas-management)
6. [Activos (Assets)](#activos-assets)
7. [Mantenimiento (Maintenance)](#mantenimiento-maintenance)
8. [Compras y Proveedores (Procurement)](#compras-y-proveedores-procurement)
9. [Telemetría (Telemetry)](#telemetría-telemetry)
10. [Alarmas (Alarming)](#alarmas-alarming)
11. [Medios y Archivos (Media)](#medios-y-archivos-media)
12. [Gestión de Identidad (Identity Management)](#gestión-de-identidad-identity-management)
13. [Sectores (Sectors)](#sectores-sectors)
14. [Auditoría y Aprobaciones (Auditing & Approvals)](#auditoría-y-aprobaciones-auditing--approvals)
15. [Configuración del Sistema (Configuration)](#configuración-del-sistema-configuration)
16. [Fuentes de Datos (Data Sources)](#fuentes-de-datos-data-sources)
17. [Notificaciones (Notifications)](#notificaciones-notifications)

---

## Dinámica de Roles y Permisos

El sistema utiliza un modelo de control de acceso basado en roles (RBAC). Los roles definen qué acciones puede realizar un usuario dentro de la plataforma. A continuación, se describen los roles predeterminados y sus responsabilidades:

### 1. GLOBAL_SUPER_ADMIN
*   **Descripción:** Es el "dueño" del sistema. Tiene acceso total e irrestricto a todos los recursos y configuraciones de la plataforma.
*   **Alcance:** Global (todos los tenants).
*   **Permisos:** Todos los permisos del sistema.

### 2. PLATFORM_ADMIN
*   **Descripción:** Encargado de la gestión operativa y comercial de la plataforma SaaS. Su foco es la administración de clientes (Tenants) y planes de suscripción, no la operación industrial.
*   **Alcance:** Global.
*   **Permisos Clave:**
    *   Gestión de Planes (Crear, Editar precios).
    *   Gestión de Tenants (Alta de empresas, Actualización de datos).
    *   Gestión de Suscripciones.
    *   Lectura global de usuarios.

### 3. TENANT_ADMIN (Gerente de Planta)
*   **Descripción:** Es el administrador principal dentro de una organización específica (Tenant). Tiene control total sobre los datos y operaciones de su propia empresa.
*   **Alcance:** Local (solo su Tenant).
*   **Permisos Clave:**
    *   **Gestión de Identidad:** Crear y administrar usuarios y roles personalizados para su equipo.
    *   **Operaciones:** Gestión completa de Activos, Mantenimiento, Compras y Almacén.
    *   **Configuración:** Definición de Sectores, Reglas de Alarma y Fuentes de Datos.
    *   **Auditoría:** Acceso a logs y aprobación de solicitudes críticas (ej. borrado de activos).

### 4. OPERATOR (Operador de Planta)
*   **Descripción:** Personal de primera línea encargado de ejecutar las tareas de mantenimiento y supervisión diaria.
*   **Alcance:** Local (solo su Tenant).
*   **Permisos Clave:**
    *   **Lectura:** Ver Activos, Órdenes de Trabajo y Alarmas.
    *   **Ejecución:** Actualizar el estado de Órdenes de Trabajo (ej. iniciar, completar) y reconocer Alarmas activas.
    *   **Restricciones:** No puede borrar registros, crear usuarios ni modificar configuraciones del sistema.

> **Nota:** El sistema permite a los `TENANT_ADMIN` crear nuevos roles personalizados con combinaciones específicas de permisos para adaptarse a las necesidades de su organización (ej. "Supervisor de Mantenimiento", "Auditor de Calidad").

---

## Visión del Modelo SaaS

Astruxa está diseñada bajo una arquitectura **Multi-Tenant con Aislamiento Lógico**. Esto significa que una única instancia de la aplicación y la base de datos sirve a múltiples clientes (Tenants), garantizando la seguridad y separación de sus datos.

### 1. Aislamiento de Datos (Data Isolation)
*   **Tenant ID:** Cada registro crítico en la base de datos (Usuarios, Activos, Órdenes, etc.) está etiquetado con un `tenant_id`.
*   **Seguridad:** El backend intercepta automáticamente todas las consultas para asegurar que un usuario solo pueda acceder a los datos de su propio Tenant. Esto es transparente para el frontend, pero vital para la seguridad.

### 2. Planes y Límites (Monetization Strategy)
El modelo de negocio se basa en **Suscripciones a Planes**. Cada plan define:
*   **Cuotas (Hard Limits):** Cantidad máxima de recursos permitidos.
    *   Ejemplo: Plan "Free" permite 5 activos y 2 usuarios. Plan "Pro" permite 100 activos y 10 usuarios.
*   **Características (Feature Flags):** Módulos habilitados o deshabilitados.
    *   Ejemplo: El módulo de "Compras Inteligentes" solo está activo en planes "Enterprise".
*   **Control:** El backend valida estos límites en tiempo real (`/api/v1/saas/usage`). Si un Tenant intenta crear un activo superando su cuota, recibirá un error `403 Forbidden` con un mensaje explicativo.

### 3. Onboarding Automatizado
El crecimiento del SaaS depende de un flujo de alta sin fricción:
1.  **Registro Público:** Cualquier empresa puede registrarse (`/api/v1/saas/public/register`).
2.  **Provisión Automática:** Al registrarse, el sistema crea automáticamente:
    *   El Tenant.
    *   El usuario administrador (`TENANT_ADMIN`).
    *   Roles predeterminados (`OPERATOR`).
    *   Una suscripción activa al plan seleccionado.
3.  **Time-to-Value:** El usuario puede empezar a operar inmediatamente después del registro.

### 4. Ecosistema de Partners
El sistema soporta la figura de **Partners** (Distribuidores). Un Partner puede agrupar varios Tenants, permitiendo modelos de negocio B2B2B (ej. una consultora de mantenimiento que gestiona el software para varias fábricas pequeñas).

---

## Visión de Arquitectura y Funcionamiento del Frontend

Como complemento a la API, el Frontend debe implementarse siguiendo una arquitectura de **Single Page Application (SPA)** modular, adaptando la interfaz según el rol del usuario autenticado.

### 1. Módulo de Onboarding (Público)
Este módulo consume los endpoints públicos de SaaS y Autenticación.
*   **Landing Page & Pricing:** Muestra los planes obtenidos de `/api/v1/saas/plans`.
*   **Registro de Empresa:** Formulario "Wizard" que recoge datos del admin y la empresa, enviándolos a `/api/v1/saas/public/register`.
*   **Login:** Pantalla de acceso centralizada (`/api/v1/auth/login`). Si el usuario tiene 2FA activado (`is_tfa_enabled: true`), redirige a la pantalla de verificación de código.

### 2. Consola de Gestión (Desktop - Tenant Admin)
Diseñada para pantallas grandes, enfocada en la administración y análisis de datos.
*   **Dashboard Principal:**
    *   **KPIs:** Widgets consumiendo `/api/v1/saas/usage` (uso de recursos) y contadores de alarmas activas.
    *   **Gráficos:** Visualización de telemetría (`/api/v1/ops/telemetry/readings/{asset_id}`) para activos críticos.
*   **Gestión de Activos:**
    *   Vista de árbol o tabla jerárquica filtrable por `Sector`.
    *   Detalle del activo con pestañas: Información General, Historial de Mantenimiento, Telemetría en vivo.
*   **Centro de Aprobaciones:**
    *   Bandeja de entrada para solicitudes pendientes (ej. borrado de activos) consumiendo `/api/v1/back-office/auditing/approvals/pending`.
*   **Gestión de Usuarios:**
    *   Tabla CRUD para usuarios y asignación de roles (`/api/v1/auth/users`).

### 3. Interfaz Operativa (Mobile First - Operator)
Diseñada para tablets o móviles, enfocada en la ejecución rápida en planta.
*   **Mis Tareas (Work Orders):**
    *   Lista filtrada de órdenes asignadas al usuario logueado.
    *   Tarjetas grandes con botones de acción rápida: "Iniciar", "Pausar", "Completar".
*   **Ejecución de Orden:**
    *   Al completar una orden, el operador debe poder subir evidencia fotográfica. El frontend debe manejar el flujo de dos pasos:
        1.  Solicitar URL de subida (`/api/v1/ops/media/upload-request`).
        2.  Subir archivo y confirmar (`.../confirm-upload`).
*   **Escáner QR (Futuro):** Para navegar rápidamente al detalle de un activo (`/api/v1/ops/assets/{uuid}`).

### 4. Componentes Transversales (Shared)
*   **Notificaciones:** Campanita en la barra superior que hace polling a `/api/v1/notifications/`.
*   **Manejo de Errores:** Interceptores HTTP que detecten `401 Unauthorized` (redirigir a login) y `403 Forbidden` (mostrar mensaje "No tienes permisos").

---

## Autenticación (Authentication)

### Login (Obtener Token)
Obtiene un token de acceso OAuth2 para autenticarse en el sistema.

*   **URL:** `/api/v1/auth/login`
*   **Método:** `POST`
*   **Cuerpo (x-www-form-urlencoded):**
    *   `username`: Email del usuario.
    *   `password`: Contraseña.
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
      "token_type": "bearer",
      "user": {
        "email": "user@example.com",
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_at": "2023-10-27T10:00:00Z",
        "updated_at": "2023-10-27T10:00:00Z",
        "is_tfa_enabled": false
      }
    }
    ```

### Obtener Usuario Actual (Me)
Obtiene la información del usuario autenticado.

*   **URL:** `/api/v1/auth/me`
*   **Método:** `GET`
*   **Auth:** Bearer Token
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
      "email": "user@example.com",
      "name": "Juan Perez",
      "is_active": true,
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "created_at": "2023-10-27T10:00:00Z",
      "updated_at": "2023-10-27T10:00:00Z",
      "is_tfa_enabled": false
    }
    ```

### Registrar Usuario
Registra un nuevo usuario en el sistema.

*   **URL:** `/api/v1/auth/register`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "email": "nuevo@empresa.com",
      "password": "passwordSeguro123",
      "name": "Nuevo Usuario",
      "role_ids": []
    }
    ```
*   **Respuesta Exitosa (201 Created):** Retorna el token y datos del usuario (similar a Login).

### Configurar 2FA (Setup TFA)
Inicia el proceso de configuración de doble factor de autenticación.

*   **URL:** `/api/v1/auth/tfa/setup`
*   **Método:** `POST`
*   **Auth:** Bearer Token
*   **Respuesta Exitosa (200 OK):** Retorna el secreto o URL para el código QR.

### Habilitar 2FA
Confirma y habilita el 2FA usando un token generado.

*   **URL:** `/api/v1/auth/tfa/enable`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "token": "123456"
    }
    ```

---

## Gestión SaaS (SaaS Management)

### Registro Público de Tenant
Permite registrar una nueva empresa (tenant) públicamente.

*   **URL:** `/api/v1/saas/public/register`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "company_name": "Mi Empresa S.A.",
      "admin_name": "Admin Principal",
      "admin_email": "admin@miempresa.com",
      "admin_password": "securePassword123",
      "plan_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    }
    ```
*   **Respuesta Exitosa (201 Created):** Retorna los datos del Tenant creado.

### Obtener Uso del Tenant
Reporte del uso de recursos actual.

*   **URL:** `/api/v1/saas/usage`
*   **Método:** `GET`
*   **Auth:** Bearer Token
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
      "users": { "used": 5, "limit": 10 },
      "assets": { "used": 20, "limit": 100 }
    }
    ```

### Listar Planes
Lista los planes de suscripción disponibles.

*   **URL:** `/api/v1/saas/plans`
*   **Método:** `GET`
*   **Respuesta Exitosa (200 OK):** Array de objetos `PlanRead`.

---

## Activos (Assets)

### Listar Activos
Obtiene una lista paginada de activos.

*   **URL:** `/api/v1/ops/assets/`
*   **Método:** `GET`
*   **Parámetros Query:** `skip`, `limit`, `type`, `sectorId`
*   **Respuesta Exitosa (200 OK):**
    ```json
    [
      {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "Motor Principal",
        "status": "operational",
        "asset_type": { "name": "Motor", "id": "..." },
        "serial_number": "SN-12345",
        "location": "Nave 1"
      }
    ]
    ```

### Crear Activo
*   **URL:** `/api/v1/ops/assets/`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "asset_type_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "sector_id": "uuid-sector",
      "serial_number": "SN-999",
      "location": "Planta Baja",
      "properties": { "potencia": "500W" }
    }
    ```

### Actualizar Estado de Activo
*   **URL:** `/api/v1/ops/assets/{asset_uuid}/status`
*   **Método:** `PATCH`
*   **Cuerpo (JSON):**
    ```json
    {
      "status": "maintenance"
    }
    ```

---

## Mantenimiento (Maintenance)

### Crear Orden de Trabajo
*   **URL:** `/api/v1/ops/maintenance/work-orders`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "title": "Reparación de Motor",
      "description": "El motor hace ruido extraño.",
      "priority": "HIGH",
      "asset_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "scheduled_start_date": "2023-11-01T09:00:00Z"
    }
    ```

### Listar Órdenes de Trabajo
*   **URL:** `/api/v1/ops/maintenance/work-orders`
*   **Método:** `GET`

### Evaluar Orden de Trabajo
Permite calificar una orden completada.

*   **URL:** `/api/v1/ops/maintenance/work-orders/{work_order_id}/evaluate`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "rating": 5,
      "feedback": "Excelente trabajo, muy rápido."
    }
    ```

---

## Compras y Proveedores (Procurement)

### Crear Proveedor
*   **URL:** `/api/v1/ops/procurement/providers`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "name": "Soluciones Industriales ACME",
      "contact_info": "contacto@acme.com",
      "specialty": "Repuestos",
      "performance_score": 95.5
    }
    ```

### Crear Repuesto (Spare Part)
*   **URL:** `/api/v1/ops/procurement/spare-parts`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "name": "Rodamiento 6203",
      "part_number": "SKF-6203",
      "price": 15.50,
      "stock_quantity": 100
    }
    ```

---

## Telemetría (Telemetry)

### Ingesta Masiva de Lecturas
*   **URL:** `/api/v1/ops/telemetry/readings`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "readings": [
        {
          "asset_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "timestamp": "2023-10-27T10:00:00Z",
          "metric_name": "temperature",
          "value": 45.5
        }
      ]
    }
    ```

### Obtener Lecturas Agregadas
Ideal para gráficos.

*   **URL:** `/api/v1/ops/telemetry/readings/{asset_id}`
*   **Método:** `GET`
*   **Parámetros Query:** `metric_name` (req), `start_time`, `end_time`, `interval` (ej: "1 hour").

---

## Alarmas (Alarming)

### Crear Regla de Alarma
*   **URL:** `/api/v1/ops/alarming/rules`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "asset_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "metric_name": "temperature",
      "condition": ">",
      "threshold": 80,
      "severity": "critical"
    }
    ```

### Listar Alarmas Activas
*   **URL:** `/api/v1/ops/alarming/alarms/active`
*   **Método:** `GET`

### Reconocer Alarma
*   **URL:** `/api/v1/ops/alarming/alarms/{alarm_id}/acknowledge`
*   **Método:** `POST`

---

## Medios y Archivos (Media)

### Solicitar Subida de Archivo
Paso 1 para subir un archivo.

*   **URL:** `/api/v1/ops/media/upload-request`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "context": "WORK_ORDER_EVIDENCE",
      "context_id": "uuid-work-order",
      "original_filename": "foto_reparacion.jpg",
      "content_type": "image/jpeg",
      "size_bytes": 102400
    }
    ```

### Confirmar Subida
Paso 2, después de subir el binario.

*   **URL:** `/api/v1/ops/media/{media_item_id}/confirm-upload`
*   **Método:** `POST`

---

## Gestión de Identidad (Identity Management)

### Listar Roles
*   **URL:** `/api/v1/back-office/identity/roles`
*   **Método:** `GET`

### Crear Rol
*   **URL:** `/api/v1/back-office/identity/roles`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "name": "Supervisor de Planta",
      "description": "Acceso a gestión de activos y órdenes.",
      "permission_ids": ["uuid-perm-1", "uuid-perm-2"]
    }
    ```

---

## Sectores (Sectors)

### Crear Sector
*   **URL:** `/api/v1/back-office/sectors/`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "name": "Línea de Montaje A",
      "description": "Sector principal de ensamblaje",
      "parent_id": null
    }
    ```

---

## Auditoría y Aprobaciones (Auditing & Approvals)

### Listar Logs de Auditoría
*   **URL:** `/api/v1/back-office/auditing/logs`
*   **Método:** `GET`

### Decidir sobre Solicitud (Aprobar/Rechazar)
*   **URL:** `/api/v1/back-office/auditing/approvals/{request_id}/decide`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "approved": true,
      "rejection_reason": null
    }
    ```

---

## Configuración del Sistema (Configuration)

### Crear Parámetro
*   **URL:** `/api/v1/sys-mgt/configuration/parameters`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "key": "SMTP_HOST",
      "value": "smtp.gmail.com",
      "description": "Servidor de correo saliente"
    }
    ```

---

## Fuentes de Datos (Data Sources)

### Crear Fuente de Datos (PLC/IoT)
*   **URL:** `/api/v1/sys-mgt/data-sources/`
*   **Método:** `POST`
*   **Cuerpo (JSON):**
    ```json
    {
      "name": "PLC Línea 1",
      "protocol": "modbus_tcp",
      "connection_params": {
        "host": "192.168.1.50",
        "port": 502
      }
    }
    ```

---

## Notificaciones (Notifications)

### Obtener Mis Notificaciones
*   **URL:** `/api/v1/notifications/`
*   **Método:** `GET`

### Marcar como Leída
*   **URL:** `/api/v1/notifications/{notification_id}/read`
*   **Método:** `POST`
