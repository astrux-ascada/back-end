# 🗺️ Roadmap Técnico - Astruxa SaaS (Industrial Orchestrator 5.0)

> **Estado del Proyecto:** Fase de Cimientos SaaS Completada (Backend Ready).
> **Objetivo:** Plataforma Multi-Tenant Global para la Industria 5.0.

---

## ✅ Hito 1: Cimientos SaaS & Seguridad (COMPLETADO)

Hemos transformado el backend monolítico en una arquitectura SaaS Enterprise robusta.

### Infraestructura & Core
- [x] **Arquitectura Multi-Tenant Híbrida:** Soporte para múltiples organizaciones con aislamiento lógico de datos (`tenant_id`).
- [x] **Modelo de Negocio:** Entidades `Partner`, `Tenant`, `Plan`, `Subscription` implementadas.
- [x] **Seguridad Zero-Trust:**
    - Login con "Gatekeeper" (validación de suscripción activa).
    - Protección contra fuerza bruta y control de concurrencia de sesiones.
    - Validación estricta de contraseñas y emails.
- [x] **Auditoría:** Sistema de logs inmutables para todas las operaciones críticas.

### Módulos Operativos (Aislados por Tenant)
- [x] **Identity:** Gestión de usuarios y roles (RBAC) por tenant.
- [x] **Assets:** Inventario de activos y jerarquías.
- [x] **Maintenance:** Órdenes de trabajo, asignaciones y flujo de estados.
- [x] **Procurement:** Proveedores y repuestos (con validación de feature flag por plan).
- [x] **Alarming:** Reglas de alerta y monitoreo en tiempo real.
- [x] **Notifications:** Sistema de notificaciones interno.

### Funcionalidades Avanzadas
- [x] **Media Manager:** Sistema seguro de subida de archivos (Local/S3) con URLs presignadas.
- [x] **Módulo de Aprobaciones:** Flujo "Maker-Checker" para acciones destructivas o críticas.

---

## 🚀 Fase 2: Frontend & Experiencia de Usuario (PRÓXIMO PASO)

**Objetivo:** Construir las interfaces que consumirán la nueva API SaaS.

### Panel de Operaciones (`/ops`)
- [ ] **Dashboard de Técnico:** Lista de OTs asignadas, escaneo de QR de activos.
- [ ] **Vista de Activo:** Detalle del activo, historial de mantenimiento, telemetría en vivo.
- [ ] **Gestor de Archivos:** Subida de evidencias (fotos/PDFs) usando el Media Manager.

### Panel Administrativo (`/back-office`)
- [ ] **Gestión de Usuarios:** Alta/Baja de técnicos, asignación de roles.
- [ ] **Configuración de Alertas:** Creación visual de reglas de alarma.
- [ ] **Auditoría:** Visualizador de logs de operaciones y aprobaciones pendientes.

### Panel de Plataforma (`/sys-mgt`)
- [ ] **Gestión de Tenants:** Alta de nuevos clientes, asignación de planes.
- [ ] **Métricas Globales:** Uso de recursos, usuarios activos por tenant.

---

## 💳 Fase 3: Automatización Comercial & Pagos

**Objetivo:** Automatizar el ciclo de vida del cliente (Onboarding/Billing).

- [ ] **Pasarela de Pagos:** Integración con Stripe/PayPal para cobro de suscripciones.
- [ ] **Portal de Cliente:** Auto-registro y gestión de métodos de pago.
- [ ] **Webhooks:** Manejo de eventos de pago (pago fallido, renovación exitosa) para actualizar el estado del tenant automáticamente.
- [ ] **Facturación:** Generación automática de facturas PDF.

---

## 🧠 Fase 4: Inteligencia Industrial (AI & Digital Twin)

**Objetivo:** Aportar valor predictivo sobre los datos recolectados.

- [ ] **Mantenimiento Predictivo:** Modelos de ML entrenados con el histórico de telemetría para predecir fallos.
- [ ] **Detección de Anomalías:** Alertas inteligentes basadas en patrones inusuales, no solo umbrales fijos.
- [ ] **Digital Twin 3D:** Visualización interactiva de la planta usando los datos en tiempo real.

---

## 🛠️ Deuda Técnica & Mantenimiento

- [ ] **Tests E2E:** Implementar pruebas automatizadas para los flujos críticos (Login -> Crear OT -> Aprobar).
- [ ] **CI/CD:** Pipeline de despliegue automático a entornos de Staging/Producción.
- [ ] **Documentación de API:** Mantener Swagger/ReDoc actualizado con ejemplos de uso.
