# ✅ IMPLEMENTADO

Esta propuesta ha sido implementada mediante la separación de routers y la lógica de servicios.

**Detalles de la Implementación:**
- **Separación de Routers:** Se han creado routers específicos bajo `/sys-mgt/` que no dependen de la suscripción del tenant (`require_active_subscription`), sino de permisos globales (`require_permission`).
- **Gestión de Usuarios Globales:** El `AuthService` y `UserRepository` ahora soportan operaciones sobre usuarios que no tienen un `tenant_id` asignado (usuarios de plataforma).

**Fecha de Implementación:** 2024-02-12
