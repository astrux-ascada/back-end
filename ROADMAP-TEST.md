# 🧪 Plan Maestro de Pruebas (Test Plan) - Astruxa Backend

> **Objetivo:** Garantizar la estabilidad, seguridad y corrección del backend antes del despliegue en GCP y el desarrollo del Frontend.
> **Herramientas:** `pytest`, `httpx` (TestClient), `alembic` (para BD de test).

Este documento sirve como lista de chequeo (checklist) para el desarrollo de la suite de pruebas automatizadas.

---

## 🛠️ 0. Configuración del Entorno de Pruebas (Infrastructure)

Antes de escribir tests, necesitamos los cimientos.

- [ ] **Configuración de `pytest`:**
    - [ ] Archivo `conftest.py` raíz configurado.
    - [ ] Fixture `db_session`: Crea una BD temporal, aplica migraciones y hace rollback tras cada test.
    - [ ] Fixture `client`: Instancia de `TestClient` de FastAPI inyectada con la `db_session`.
    - [ ] Fixture `auth_headers`: Helper para obtener headers de autenticación de usuarios de prueba (Super Admin, Tenant Admin, Operador).
    - [ ] Fixture `mock_redis`: Mockear Redis para no depender de un servicio externo en tests unitarios.

---

## 🧱 1. Tests Unitarios (Lógica de Negocio Pura)

Verificar funciones individuales y métodos de servicios aislados de la BD y HTTP.

### 1.1 Core & Utilidades
- [ ] `app/core/security.py`: Hashing de contraseñas, generación de tokens JWT.
- [ ] `app/core/context.py`: Gestión de ContextVars (tenant_id, user_id).

### 1.2 Servicios de Dominio (Mocks de Repositorios)
- [ ] **SaaS Service:** Cálculo de prorrata en upgrades de plan.
- [ ] **Alarming Service:** Evaluación de reglas (¿El valor X dispara la regla Y?).
- [ ] **Procurement Service:** Lógica de selección de mejor cotización (SSI).

---

## 🔗 2. Tests de Integración (API Endpoints & Flujos)

Verificar que los endpoints funcionan correctamente, interactúan con la BD y devuelven los códigos de estado adecuados.

### 2.1 Autenticación & Identidad (`/auth`)
- [ ] **Login:**
    - [ ] Login exitoso (retorna token).
    - [ ] Login fallido (credenciales incorrectas).
    - [ ] Login con usuario inactivo.
- [ ] **Gestión de Usuarios:**
    - [ ] Crear usuario (como Admin).
    - [ ] Listar usuarios (paginación).
    - [ ] Actualizar usuario propio.
    - [ ] Eliminar usuario.

### 2.2 Gestión SaaS (`/saas`)
- [ ] **Registro Público:** Flujo completo de registro de nuevo tenant + usuario admin.
- [ ] **Planes:** CRUD de planes (solo Super Admin).
- [ ] **Tenants:** Listado y detalles de tenants.

### 2.3 Operaciones - Activos (`/ops/assets`)
- [ ] **CRUD Activos:**
    - [ ] Crear activo (verificar `tenant_id` automático).
    - [ ] Leer activo (verificar filtrado por tenant).
    - [ ] Actualizar activo.
    - [ ] Borrado lógico (Soft Delete).
- [ ] **Jerarquía:** Asignar padre/hijo y verificar estructura.

### 2.4 Operaciones - Mantenimiento (`/ops/maintenance`)
- [ ] **Órdenes de Trabajo (OT):**
    - [ ] Crear OT.
    - [ ] Asignar OT a usuario.
    - [ ] Cambiar estado de OT (Open -> In Progress -> Completed).
    - [ ] Cancelar OT.

### 2.5 Operaciones - Compras (`/ops/procurement`)
- [ ] **Proveedores & Repuestos:**
    - [ ] Crear proveedor.
    - [ ] Crear repuesto asociado a proveedor.
    - [ ] Actualizar stock de repuesto.

### 2.6 Core Engine & Telemetría
- [ ] **Ingesta de Datos:**
    - [ ] Endpoint de recepción masiva de lecturas.
    - [ ] Verificar que las lecturas se guardan en la BD (Timescale/Postgres).
- [ ] **Consulta:**
    - [ ] Endpoint de datos agregados (promedios, min, max).

---

## 🛡️ 3. Tests de Seguridad & Permisos (RBAC)

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

## 🚀 4. Tests de Rendimiento (Opcional / Fase Posterior)

- [ ] **Locust/K6:** Prueba de carga sobre el endpoint de ingesta de telemetría (simular 1000 dispositivos enviando datos).

---

## ✅ Estado de Ejecución

| Módulo | Unitarios | Integración | Seguridad | Estado |
| :--- | :---: | :---: | :---: | :---: |
| **Core / Config** | ⬜ | ⬜ | N/A | ⏳ Pendiente |
| **Auth / Identity** | ⬜ | ⬜ | ⬜ | ⏳ Pendiente |
| **SaaS / Tenants** | ⬜ | ⬜ | ⬜ | ⏳ Pendiente |
| **Assets** | ⬜ | ⬜ | ⬜ | ⏳ Pendiente |
| **Maintenance** | ⬜ | ⬜ | ⬜ | ⏳ Pendiente |
| **Procurement** | ⬜ | ⬜ | ⬜ | ⏳ Pendiente |
| **Telemetría** | ⬜ | ⬜ | N/A | ⏳ Pendiente |
