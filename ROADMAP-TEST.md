# 🧪 Plan Maestro de Pruebas (Test Plan) - Astruxa Backend

> **Objetivo:** Garantizar la estabilidad, seguridad y corrección del backend antes del despliegue en GCP y el desarrollo del Frontend.
> **Estado Actual:** Infraestructura básica y tests de autenticación completados. Faltan tests de lógica de negocio crítica (SaaS, Operaciones).

Este documento sirve como lista de chequeo (checklist) para el desarrollo de la suite de pruebas automatizadas.

---

## 🛠️ 0. Configuración del Entorno de Pruebas (Infrastructure)

✅ **Completado:** La infraestructura base ya está operativa.
- [x] **Configuración de `pytest`:** `conftest.py` raíz configurado.
- [x] **Fixtures:** `db_session`, `client` y `auth_headers` implementados.
- [x] **CI/CD:** Pipeline básico de ejecución de tests.

---

## 🧱 1. Tests Unitarios (Lógica de Negocio Pura)

Verificar funciones individuales y métodos de servicios aislados de la BD y HTTP.

### 1.1 Core & Utilidades
- [x] `app/core/security.py`: Hashing de contraseñas, JWT (`tests/core/test_security.py`).
- [x] `app/core/email.py`: Envío de correos (`tests/core/test_email.py`).
- [ ] `app/core/context.py`: Gestión de ContextVars (tenant_id, user_id).

### 1.2 Servicios de Dominio (Mocks de Repositorios)
- [ ] **SaaS Service:** Cálculo de prorrata en upgrades de plan.
- [ ] **Alarming Service:** Evaluación de reglas (¿El valor X dispara la regla Y?).
- [ ] **Procurement Service:** Lógica de selección de mejor cotización (SSI).

---

## 🔗 2. Tests de Integración (API Endpoints & Flujos)

Verificar que los endpoints funcionan correctamente, interactúan con la BD y devuelven los códigos de estado adecuados.

### 2.1 Autenticación & Identidad (`/auth`)
✅ **Completado:** `tests/api/test_auth_flow.py` cubre login, registro y tokens.
- [x] **Login:** Exitoso, fallido, usuario inactivo.
- [x] **Registro:** Creación de usuario.
- [ ] **Gestión de Usuarios:** Listar, actualizar, eliminar (Falta cobertura).

### 2.2 Gestión SaaS (`/saas`) - 🚨 CRÍTICO (FALTANTE)
No existen pruebas para la lógica multi-tenant ni límites de planes.
- [ ] **Registro Público:** Flujo completo de registro de nuevo tenant + usuario admin.
- [ ] **Planes:** CRUD de planes (solo Super Admin).
- [ ] **Límites de Plan:** Verificar que no se pueden crear más activos de los permitidos por el plan.
- [ ] **Tenants:** Listado y detalles de tenants.

### 2.3 Operaciones - Activos (`/ops/assets`) - 🚨 CRÍTICO (FALTANTE)
- [ ] **CRUD Activos:** Crear, Leer, Actualizar, Borrado lógico.
- [ ] **Jerarquía:** Asignar padre/hijo y verificar estructura.
- [ ] **Tipos de Activo:** Crear y listar tipos.

### 2.4 Operaciones - Mantenimiento (`/ops/maintenance`) - 🚨 CRÍTICO (FALTANTE)
- [ ] **Órdenes de Trabajo (OT):**
    - [ ] Crear OT.
    - [ ] Asignar OT a usuario.
    - [ ] Cambiar estado de OT (Open -> In Progress -> Completed).
    - [ ] Cancelar OT.

### 2.5 Operaciones - Compras (`/ops/procurement`) - 🚨 CRÍTICO (FALTANTE)
- [ ] **Proveedores & Repuestos:**
    - [ ] Crear proveedor.
    - [ ] Crear repuesto asociado a proveedor.
    - [ ] Actualizar stock de repuesto.

### 2.6 Core Engine & Telemetría
- [ ] **Ingesta de Datos:** Endpoint de recepción masiva.
- [ ] **Consulta:** Endpoint de datos agregados.
- [ ] **Alarmas:** Verificar que una lectura anómala crea una alarma.

### 2.7 Media Manager (`/ops/media`)
✅ **Completado:** `tests/api/test_media_flow.py` cubre subida de archivos.
- [x] **Subida:** Solicitar URL, subir archivo, confirmar.

---

## 🛡️ 3. Tests de Seguridad & Permisos (RBAC) - 🚨 CRÍTICO (FALTANTE)

Verificar que nadie puede acceder a donde no debe.

- [ ] **Aislamiento de Tenants (Multi-Tenancy):**
    - [ ] **Test Crítico:** Crear dos tenants (A y B). Crear activo en A. Intentar leer activo de A con usuario de B. **Debe fallar (404 o 403).**
- [ ] **Roles y Permisos:**
    - [ ] Intentar crear usuario con rol de "Operador" -> Debe fallar (403).
    - [ ] Intentar acceder a endpoints de `/sys-mgt` con usuario no Super Admin -> Debe fallar.
- [ ] **Autenticación:**
    - [ ] Acceder a endpoints protegidos sin token -> 401.
    - [ ] Acceder con token expirado -> 401.

---

## ✅ Estado de Ejecución

| Módulo | Unitarios | Integración | Seguridad | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **Core / Config** | ✅ | 🚧 | N/A | 🟡 Parcial |
| **Auth / Identity** | ✅ | ✅ | 🚧 | 🟢 Bueno |
| **Media** | N/A | ✅ | ✅ | 🟢 Bueno |
| **SaaS / Tenants** | ⬜ | ⬜ | ⬜ | 🔴 Crítico |
| **Assets** | ⬜ | ⬜ | ⬜ | 🔴 Crítico |
| **Maintenance** | ⬜ | ⬜ | ⬜ | 🔴 Crítico |
| **Procurement** | ⬜ | ⬜ | ⬜ | 🔴 Crítico |
| **Telemetría** | ⬜ | ⬜ | N/A | 🔴 Crítico |

> **Leyenda:** ✅ Completado | 🚧 En Progreso | ⬜ Pendiente | 🔴 Bloqueante para Release
