# 🚀 Módulo de Marketing y Crecimiento

El módulo de Marketing es el motor de crecimiento de Astruxa. Permite a los administradores gestionar estrategias de adquisición y retención de clientes mediante **Campañas**, **Cupones de Descuento** inteligentes y un **Sistema de Referidos** viral.

---

## 🧠 Conceptos Clave

### 1. Campañas (`MarketingCampaign`)
Son el contenedor de alto nivel para agrupar estrategias. Permiten medir el ROI de iniciativas específicas.
*   **Ejemplos:** "Black Friday 2024", "Lanzamiento V2", "Recuperación de Clientes".
*   **Datos:** Nombre, descripción, fechas de inicio/fin y presupuesto (opcional).

### 2. Cupones (`Coupon`)
Son las herramientas tácticas que otorgan el beneficio. Este módulo soporta una lógica de descuentos avanzada para modelos SaaS.

*   **Tipos de Descuento:**
    *   `PERCENTAGE`: Descuento porcentual (ej. 20% OFF).
    *   `FIXED_AMOUNT`: Descuento monetario directo (ej. $50 USD OFF).

*   **Duración del Beneficio (Clave para SaaS):**
    *   `ONCE`: Se aplica una sola vez (ej. descuento en la primera factura).
    *   `REPEATING`: Se aplica durante un número específico de meses (ej. "50% de descuento los primeros 3 meses").
    *   `FOREVER`: Se aplica indefinidamente mientras la suscripción esté activa.

*   **Restricciones:**
    *   Fecha de expiración.
    *   Límite global de usos (ej. "Solo para los primeros 100 clientes").

### 3. Referidos (`Referral`)
Sistema para incentivar el crecimiento orgánico.
*   Cada Tenant tiene un **Código de Referido Único**.
*   El sistema rastrea quién invitó a quién (`referrer` -> `referee`).
*   Estado del referido: `PENDING` (registrado) -> `CONVERTED` (primer pago realizado).

---

## 🛠️ Arquitectura Técnica

### Modelo de Datos
El módulo introduce tres nuevas tablas principales y modifica dos existentes:

1.  **`marketing_campaigns`**: Tabla padre.
2.  **`coupons`**: Tabla hija de campañas. Contiene la lógica de validación.
3.  **`referrals`**: Tabla de relación N:M entre Tenants (quién invita y quién es invitado).
4.  **`subscriptions` (Modificada)**:
    *   `applied_coupon_id`: Referencia al cupón activo.
    *   `final_price`: El precio calculado después de aplicar el descuento.
5.  **`tenants` (Modificada)**:
    *   `referral_code`: Código único para compartir.

### Servicio: `MarketingService`
Centraliza toda la lógica de negocio en `app/identity/service_marketing.py`.
*   **Validación:** Verifica si un cupón es válido, está activo, no ha expirado y no ha superado su límite de usos.
*   **Aplicación:** Calcula el `final_price` basándose en el plan actual y el tipo de cupón, y actualiza la suscripción.

---

## 🔌 API Reference

### 1. Gestión (SysAdmin / Platform Admin)
Endpoints protegidos para la creación y gestión de campañas.
*   **Base URL:** `/api/v1/sys-mgt/marketing`

| Método | Endpoint | Descripción | Permiso Requerido |
| :--- | :--- | :--- | :--- |
| `POST` | `/campaigns` | Crear una nueva campaña. | `campaign:create` |
| `GET` | `/campaigns` | Listar todas las campañas. | `campaign:read` |
| `POST` | `/coupons` | Crear un nuevo cupón. | `coupon:create` |
| `GET` | `/coupons` | Listar todos los cupones. | `coupon:read` |

### 2. Cliente (Self-Service)
Endpoints para que los clientes utilicen las funciones de marketing.
*   **Base URL:** `/api/v1/saas`

| Método | Endpoint | Descripción | Permiso Requerido |
| :--- | :--- | :--- | :--- |
| `POST` | `/me/subscription/apply-coupon` | Aplicar un cupón a la propia suscripción. | `coupon:apply` |
| `GET` | `/me/referral-code` | Obtener el código de referido propio para compartir. | N/A (Autenticado) |

---

## 🔐 Seguridad y Permisos

El módulo introduce un set específico de permisos RBAC para controlar el acceso:

*   **Gestión de Campañas:** `campaign:create`, `campaign:read`, `campaign:update`, `campaign:delete`.
*   **Gestión de Cupones:** `coupon:create`, `coupon:read`, `coupon:update`, `coupon:delete`.
*   **Uso de Cupones:** `coupon:apply` (Asignado por defecto a los administradores de tenant).
*   **Referidos:** `referral:read`.

> **Nota:** Los roles `GLOBAL_SUPER_ADMIN` y `PLATFORM_ADMIN` tienen acceso completo a la gestión por defecto.

---

## 📝 Ejemplos de Uso

### Crear un cupón de "3 Meses al 50%"
```json
POST /api/v1/sys-mgt/marketing/coupons
{
  "code": "STARTUP50",
  "name": "Descuento de Lanzamiento",
  "discount_type": "percentage",
  "discount_value": 50.0,
  "duration": "repeating",
  "duration_in_months": 3,
  "max_redemptions": 500
}
```

### Aplicar un cupón (Cliente)
```json
POST /api/v1/saas/me/subscription/apply-coupon
{
  "coupon_code": "STARTUP50"
}
```
