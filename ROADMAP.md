# 🗺️ Roadmap Estratégico - Astruxa SaaS (Industrial Orchestrator 5.0)

> **Estado del Proyecto:** Hito 1 (Fundación SaaS) Completado.
> **Visión:** Convertir Astruxa en una plataforma SaaS comercial, escalable y líder en la Industria 5.0.

---

## ✅ Hito 1: Fundación SaaS & Seguridad (COMPLETADO)

Se ha completado la refactorización del backend a una arquitectura Multi-Tenant segura y robusta. El motor está listo.

---

## 🚀 Fase 2: Producto Mínimo Viable y Seguro (MVP) — (Criticidad: 🔴 ALTA)

**Objetivo:** Implementar las funcionalidades mínimas para poder vender, operar y facturar el producto de forma segura.

### Prioridad 1: Gestión de la Plataforma (SaaS Core)
- **Descripción:** Endpoints para que el `GLOBAL_SUPER_ADMIN` pueda crear y gestionar los componentes básicos del negocio.
- **Tareas:**
  - [x] **CRUD para `Plans`:** Crear, actualizar y desactivar planes de precios.
  - [x] **Gestión de `Tenants`:** Crear nuevos clientes y asignarles suscripciones.
  - [x] **Gestión de `Subscriptions`:** Modificar manualmente la suscripción de un cliente.

### Prioridad 2: Funcionalidad Operativa Completa (CRUDs)
- **Descripción:** Añadir las operaciones de Update y Delete (soft delete) que faltan para que el producto se sienta completo y usable.
- **Tareas:**
  - [x] **Procurement:** `PUT`/`DELETE` para Proveedores y Repuestos.
  - [x] **AlarmRule:** `PUT`/`PATCH`/`DELETE` para Reglas de Alarma.
  - [x] **Assets:** `DELETE` (soft delete) para Activos, integrado con el Módulo de Aprobaciones.
  - [x] **WorkOrder:** `PATCH` para cancelar órdenes y `POST` para asignar proveedores externos.
  - [x] **Sectors:** `PUT`/`DELETE` para Sectores.
  - [x] **Configuration:** `POST`/`DELETE` (soft delete) para parámetros globales.
  - [x] **DataSource:** Implementar CRUD completo.

### Prioridad 3: RBAC Avanzado y Seguridad de Acceso
- **Descripción:** Pasar de roles fijos a un sistema de permisos granulares para que los clientes puedan gestionar sus propios equipos.
- **Tareas:**
  - [x] Crear dependencia `require_permission(permission_name: str)`.
  - [x] Reemplazar `Depends(get_current_admin_user)` con el nuevo sistema en todos los endpoints.
  - [x] Actualizar el script de Seeding para crear permisos y asignarlos a roles por defecto.

---

## 💳 Fase 3: Automatización Comercial y Retención — (Criticidad: 🟡 MEDIA)

**Objetivo:** Convertir el producto en un negocio que escala y retiene clientes con mínima intervención manual.

### Prioridad 4: Modularización por Monetización (Feature Flags)
- **Descripción:** Implementar la lógica de negocio de los planes (Bueno, Mejor, Excelente) para justificar diferentes precios.
- **Tareas:**
  - [x] Proteger todos los routers de módulos con la dependencia `require_feature`.
  - [x] Implementar lógica `check_limit` en los servicios (ej: límite de usuarios o activos).

### Prioridad 5: Sistema de Pagos y Auto-Suscripción
- **Descripción:** Permitir que los clientes se registren y paguen por sí mismos.
- **Tareas:**
  - [ ] **Sistema de Pagos Flexible:**
    - [ ] **Interfaz de Pasarela:** Definir un contrato común para todas las pasarelas.
    - [ ] **Implementación de PayPal:** Integrar con la pasarela de PayPal.
    - [ ] **Implementación de Pasarela Configurable:** Crear una pasarela genérica.
    - [ ] **Flujo de Pago Manual (Transferencia):** Implementar un sistema para que los clientes suban comprobantes de pago y los administradores los aprueben.
  - [ ] **Portal de Auto-Suscripción:** Crear flujo de registro público y "provisioning" automático de tenants.

### Prioridad 6: Portal de Gestión de Cuenta (Customer Portal)
- **Descripción:** Reducir costos de soporte permitiendo a los clientes autogestionarse.
- **Tareas:**
  - [ ] UI para cambiar de plan, ver uso, actualizar método de pago y ver facturas.
  - [ ] **Acceso Restringido para Pagos:** Implementar el "modo de gracia" para que los `TENANT_ADMIN` puedan acceder a facturación si su pago ha fallado.

### Prioridad 7: Expansión de Canales (Portal de Partners)
- **Descripción:** Habilitar canales de venta indirectos para escalar el crecimiento.
- **Tareas:**
  - [ ] Dashboard para que los partners gestionen a sus clientes y comisiones.

---

## 🧠 Fase 4: Madurez, Inteligencia y Escalabilidad — (Criticidad: 🟢 BAJA)

**Objetivo:** Asegurar la salud a largo plazo del proyecto, añadir valor con IA y prepararse para un crecimiento masivo.

### Prioridad 8: Recopilación de Datos para IA
- **Descripción:** Implementar los mecanismos de feedback que alimentarán los futuros modelos de IA.
- **Tareas:**
  - [ ] **Evaluación de `WorkOrder`:** UI y API para que los supervisores califiquen la ejecución de las tareas.
  - [ ] **Recepción de Órdenes de Compra:** UI y API para registrar la recepción de pedidos y evaluar a los proveedores.

### Prioridad 9: Calidad y Automatización (DevEx)
- **Descripción:** Implementar una estrategia de testing y despliegue robusta.
- **Tareas:**
  - [ ] **Estrategia de Testing:** Implementar tests unitarios, de integración y E2E.
  - [ ] **Pipeline de CI/CD:** Automatizar los tests y el despliegue a Staging/Producción.

### Prioridad 10: Arquitectura a Escala
- **Descripción:** Evolucionar la arquitectura para soportar un crecimiento masivo.
- **Tareas:**
  - [ ] **Arquitectura Orientada a Eventos (EDA):** Desacoplar servicios con un Message Broker.
  - [ ] **Gestión del Ciclo de Vida de Datos (ILM):** Políticas para archivar datos de telemetría antiguos.
  - [ ] **Migración a Kubernetes (K8s):** Plan para mover la infraestructura de producción a K8s.
