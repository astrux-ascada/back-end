# 🔔 Módulo: Notificaciones — El Sistema Nervioso de la Plataforma

> **Un sistema centralizado para informar a usuarios y administradores sobre eventos críticos y acciones requeridas, tanto a nivel de cliente (Tenant) como de plataforma (Platform).**

---

## 🎯 Propósito

El **Módulo de Notificaciones** es el subsistema responsable de:

-   **Alertar en tiempo real:** Informar a los usuarios correctos sobre eventos importantes tan pronto como ocurren.
-   **Centralizar la comunicación:** Proporcionar un único lugar (la "campanita") donde los usuarios pueden ver todas sus alertas y mensajes.
-   **Guiar la acción del usuario:** Incluir enlaces directos en las notificaciones para que los usuarios puedan actuar de inmediato (ej: "Ver solicitud de aprobación").
-   **Diferenciar audiencias:** Separar claramente las notificaciones que son para los clientes (operativas) de las que son para los administradores de la plataforma (gestión).

> Sin este módulo, los usuarios operan a ciegas. Con él, la plataforma se vuelve proactiva, guiando a los usuarios hacia lo que necesita su atención.

---

## 🧩 Componentes Internos

```
[ Otros Módulos (SaaS, Maintenance, Alarming) ]
         │
         └───> [ NotificationService ]  (Crea y gestiona notificaciones)
                     │
                     └───> [ Base de Datos (tabla `notifications`) ]
                                 │
                                 └───> [ NotificationAPI ] (Expone las notificaciones al frontend)
                                             │
                                             └───> [ 🖥️ Frontend (UI de Notificaciones) ]
```

---

## 🗃️ Modelo de Datos: Tabla `notifications`

```sql
CREATE TYPE notification_level AS ENUM ('TENANT', 'PLATFORM');

CREATE TABLE notifications (
    id UUID PRIMARY KEY,
    recipient_id UUID NOT NULL, -- A quién se le muestra
    tenant_id UUID,             -- NULL si es a nivel de plataforma
    level notification_level NOT NULL, -- 'TENANT' o 'PLATFORM'
    
    icon VARCHAR(50),           -- ej: 'bell', 'warning', 'check-circle'
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    action_url TEXT,            -- ej: '/approvals/request/uuid-...'
    
    read_at TIMESTAMPTZ,        -- NULL si no está leída
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## 📈 Niveles de Notificación

### 1. Nivel `PLATFORM`
-   **Propósito:** Notificaciones para los administradores del sistema (`PLATFORM_ADMIN`, `GLOBAL_SUPER_ADMIN`).
-   **Visibilidad:** Solo visibles para estos roles. No son visibles para los clientes.
-   **Ejemplos:**
    -   "Nueva solicitud de aprobación para borrar el tenant 'Cliente XYZ'".
    -   "Un nuevo cliente, 'Empresa ABC', se ha registrado en el plan Pro".
    -   "Error en el sistema de pagos: no se pudo procesar una factura".

### 2. Nivel `TENANT`
-   **Propósito:** Notificaciones operativas para los usuarios de un cliente específico.
-   **Visibilidad:** Aisladas por `tenant_id`. Un usuario solo ve las notificaciones de su propia empresa.
-   **Ejemplos:**
    -   "Nueva orden de trabajo asignada: 'Revisar motor de la línea 2'".
    -   "Alarma crítica en 'Prensa Hidráulica': Presión excedida".
    -   "El repuesto 'Rodamiento 6203' está por debajo del stock mínimo".

---

## ⚙️ API Endpoints (`/api/v1/notifications`)

-   **`GET /`**: Obtiene la lista de notificaciones para el usuario autenticado.
    -   Permite filtrar por no leídas (`unread_only=true`).
    -   Devuelve las más recientes primero.
-   **`POST /{notification_id}/read`**: Marca una notificación específica como leída.
-   **`POST /read-all`**: Marca todas las notificaciones del usuario como leídas.

---

## 🧪 Ejemplo de Flujo: Notificación de Aprobación

1.  **Acción:** Un `PLATFORM_ADMIN` (Admin A) solicita eliminar el tenant "Cliente XYZ" a través de la API.
2.  **Servicio `SaasService`:**
    -   Recibe la solicitud.
    -   Llama al `ApprovalService` para crear la solicitud de aprobación.
    -   Llama al `NotificationService` con la función `create_platform_notification_for_role()`.
3.  **Servicio `NotificationService`:**
    -   Busca a todos los usuarios con el rol `PLATFORM_ADMIN`.
    -   Crea una notificación en la base de datos para cada uno de ellos (incluyendo al Admin A que la solicitó y a otros como el Admin B).
    -   La notificación tiene `level='PLATFORM'`, el título "Solicitud de borrado..." y un `action_url` que apunta a la página de aprobaciones.
4.  **Frontend (Admin B):**
    -   La UI de notificaciones (la "campanita") hace una llamada a `GET /api/v1/notifications/` y muestra un indicador de nueva notificación.
    -   El Admin B abre el panel, ve la notificación, hace clic en ella y es redirigido a la `action_url` para ver y aprobar/rechazar la solicitud.

⏱️ **Resultado:** El flujo de trabajo es guiado por la plataforma, reduciendo el tiempo de respuesta y asegurando que las acciones críticas no se queden en el limbo.
