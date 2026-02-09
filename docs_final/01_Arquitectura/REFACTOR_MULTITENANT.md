# Plan Estratégico de Refactorización: Arquitectura Multi-Tenant Global (Astruxa 5.0)

**Estado:** DEFINITIVO  
**Objetivo:** Transformar la arquitectura a un modelo SaaS Enterprise Global, seguro y centrado en el humano (Industry 5.0).

---

## 1. Arquitectura Comercial (Modelo de Expansión Global)

### 1.1. Entidades de Negocio (Schema `public`)

1.  **`partners` (Operadores Regionales):**
    *   Revendedores/Operadores locales (ej: Astruxa México).
    *   Gestionan sus propios Tenants.

2.  **`tenants` (Clientes Finales):**
    *   Vinculados a un Partner.
    *   Estado de ciclo de vida: `PROVISIONING`, `ACTIVE`, `SUSPENDED`, `ARCHIVED`.
    *   Configuración de aislamiento (Shared vs Dedicated DB).

3.  **`plans` (Catálogo de Productos):**
    *   Definición flexible de cuotas y features vía JSONB.

4.  **`subscriptions` (Contratos):**
    *   Controla el acceso. Estados: `TRIAL`, `ACTIVE`, `PAST_DUE`, `CANCELED`.

---

## 2. Seguridad Operacional: Human-in-the-Loop (Industry 5.0)

Implementamos el principio de "Los Cuatro Ojos" para acciones críticas.

### 2.1. Módulo de Aprobaciones (`approval_requests`)
En lugar de ejecutar acciones destructivas directamente, se crea una solicitud.

*   **Flujo:**
    1.  **Solicitante (Maker):** Pide borrar un Activo -> Se crea `ApprovalRequest`.
    2.  **Sistema:** Marca el activo como `PENDING_DELETION` (Soft Lock).
    3.  **Aprobador (Checker):** Revisa justificación y Aprueba/Rechaza.
    4.  **Ejecución:** Si se aprueba, se ejecuta la acción final.

*   **Configurabilidad:**
    *   El Cliente (`TENANT_ADMIN`) define qué acciones requieren aprobación y quién las aprueba.

---

## 3. Segregación de API y Roles

*   **`/sys-mgt`:** Gestión Global y Regional (Partners).
*   **`/back-office`:** Gestión Administrativa del Cliente (Gerentes).
*   **`/ops`:** Operación Diaria (Técnicos).

---

## 4. Seguridad y Compliance

*   **Gatekeeper:** Login bloqueado para impagos (salvo admins).
*   **Trazabilidad Legal:** Tabla `user_agreements` para aceptación de términos.
*   **Media Manager:** Gestión de archivos aislada por Tenant.

---

## 5. Plan de Ejecución (Fase 1: Cimientos SaaS)

Vamos a implementar los modelos base que soportan toda esta estructura.

1.  **`app/identity/models/saas/partner.py`**
2.  **`app/identity/models/saas/plan.py`**
3.  **`app/identity/models/saas/tenant.py`**
4.  **`app/identity/models/saas/subscription.py`**
5.  **Refactorizar `User`** para incluir `tenant_id` y `agreement_version`.
