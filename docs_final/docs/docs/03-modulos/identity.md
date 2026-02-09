
En un sistema industrial 5.0, donde un comando mal ejecutado puede parar una línea, dañar una máquina o exponer secretos de producción… **la seguridad no es una característica. Es la base.**

---

## 📄 `03-modulos/identity.md` — LISTO PARA COPIAR Y PEGAR

```markdown
# 🔐 Módulo: Identity — Autenticación, Autorización y Gestión de Acceso Industrial (Zero Trust)

> **Sistema de identidad y acceso con Zero Trust, MFA obligatorio, RBAC granular por máquina/acción, y auditoría inmutable — diseñado para proteger secretos industriales, prevenir sabotajes y garantizar que solo las personas correctas hagan las acciones correctas, en el momento correcto.**

---

## 🎯 Propósito

El **Identity Module** es el subsistema responsable de:

- **Autenticar usuarios** con MFA obligatorio para acciones críticas.
- **Autorizar accesos** con roles y permisos granulares (por máquina, acción, zona, turno).
- **Gestionar sesiones** con expiración corta y revocación en tiempo real.
- **Auditar todas las acciones** de acceso y comandos (quién, cuándo, qué, desde dónde).
- **Integrarse con SSO corporativo** (Active Directory, Azure AD, Okta).
- **Proteger APIs y endpoints** con JWT, OAuth2 y políticas de seguridad.
- **Aplicar arquitectura Zero Trust**: nunca confiar, siempre verificar.

> En una fábrica digital, **la seguridad no es un firewall. Es un sistema vivo que autentica, autoriza y audita cada interacción — desde ver un sensor hasta detener una línea.**

---

## 🧩 Componentes Internos

```
[ User Login ] → [ Auth Engine (JWT + MFA) ]
                   ↓
          [ Policy Decision Point ]
                   ↓
         [ Role & Permission Evaluator ]
                   ↓
          [ Session Manager + Vault ]
                   ↓
           [ API Gateway + Audit Log ]
```

---

## 🆔 Auth Engine (Motor de Autenticación)

- **Función**: Verifica identidad del usuario + MFA.
- **Flujo de login**:
  1. Usuario ingresa email + contraseña.
  2. Sistema valida credenciales (contra PostgreSQL o SSO).
  3. Si intenta acción crítica → exige MFA.
  4. MFA soportados:
     - App Authenticator (Google/Microsoft).
     - SMS (solo si app no disponible).
     - Llave física (FIDO2/WebAuthn) → ideal para jefes de planta.
     - Código por email (fallback).
  5. Si MFA correcto → emite JWT con claims de rol y permisos.

> ✅ JWT con expiración corta: 15 min para acciones críticas, 1h para lectura.

---

## 🎭 Role & Permission Evaluator (Evaluador de Roles y Permisos)

- **Función**: Decide qué puede hacer un usuario, basado en:
  - Rol asignado (operario, supervisor, técnico, gerente, admin).
  - Permisos granulares por:
    - Máquina (ej: solo Línea 3).
    - Acción (ver, controlar, configurar, detener).
    - Zona de planta.
    - Turno (solo si está en turno activo).
- **Tabla `user_permissions`**:
  ```sql
  CREATE TABLE user_permissions (
      id SERIAL PRIMARY KEY,
      user_id INTEGER REFERENCES users(id),
      machine_id INTEGER REFERENCES assets(id), -- NULL = todas
      action VARCHAR(50) NOT NULL, -- 'view', 'control', 'configure', 'emergency_stop'
      zone VARCHAR(100),          -- 'Line 3', 'Warehouse', NULL = todas
      valid_during_shift BOOLEAN DEFAULT FALSE, -- solo si está en turno
      created_at TIMESTAMPTZ DEFAULT NOW()
  );
  ```
- **Ejemplos**:
  - “Carlos (técnico) → puede CONTROLAR máquinas de Línea 3, solo en su turno.”
  - “Ana (supervisor) → puede VER todas las líneas, CONTROLAR solo Línea 2.”
  - “Luis (gerente) → puede DETENER cualquier máquina (con MFA).”

---

## 🔄 Session Manager + Vault (Gestor de Sesiones y Secretos)

- **Función**: Gestiona sesiones activas y protege secretos sensibles.
- **Características**:
  - Revocación de sesiones en tiempo real (si usuario es despedido o cambia rol).
  - Almacenamiento de secretos en **HashiCorp Vault** (tokens, claves de API, credenciales de PLC).
  - Rotación automática de secretos cada 30 días.
  - Acceso a secretos solo para servicios autorizados (ej: Core Engine para conectarse a PLCs).

> ✅ Nada de credenciales hardcodeadas. Todo en Vault, con políticas de acceso.

---

## 🚦 Policy Decision Point (Punto de Decisión de Políticas)

- **Función**: Intercepta cada petición a la API y decide si se permite.
- **Integración con API Gateway** (FastAPI middleware o proxy como Kong/Tyk).
- **Verifica**:
  - JWT válido y no expirado.
  - Rol y permisos para el recurso solicitado.
  - Si requiere MFA adicional (para acciones críticas).
  - Si el usuario está en turno (si aplica).
- **Respuesta**: 200 OK o 403 Forbidden + log de intento.

---

## 📜 Audit Log (Registro de Auditoría Inmutable)

- **Función**: Registra TODAS las acciones de acceso y comandos.
- **Tabla `access_audit_log`** (¡NUNCA se borra!):
  ```sql
  CREATE TABLE access_audit_log (
      id BIGSERIAL PRIMARY KEY,
      timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      user_id INTEGER REFERENCES users(id),
      action VARCHAR(100) NOT NULL, -- 'login', 'view_machine', 'control_machine', 'emergency_stop'
      resource VARCHAR(200),        -- 'machine_7', 'sensor_TEMP_MOTOR', 'PO_205'
      ip_address VARCHAR(45),
      user_agent TEXT,
      success BOOLEAN NOT NULL,
      mfa_used BOOLEAN DEFAULT FALSE,
      session_id VARCHAR(100),
      metadata JSONB                -- detalles adicionales
  );
  ```
- **Protección**:
  - Solo lectura para aplicaciones.
  - Backup diario + firma digital (para integridad).
  - Retención: 10 años (cumplimiento normativo).

---

## 🔗 SSO Integration (Integración con Directorio Corporativo)

- **Función**: Permitir login con cuentas corporativas (no gestionar usuarios manualmente).
- **Protocolos soportados**:
  - SAML 2.0 (para Active Directory).
  - OpenID Connect (para Azure AD, Okta, Google Workspace).
- **Sincronización de roles**:  
  Grupos de AD → mapeados a roles del sistema (ej: “CN=Maintenance_Team” → rol “technician”).

---

## 🛡️ Zero Trust Architecture (Arquitectura de Confianza Cero)

- **Principios**:
  - **Nunca confiar, siempre verificar**: cada petición se autentica y autoriza, aunque venga de dentro de la red.
  - **Acceso mínimo**: solo lo necesario, solo cuando es necesario.
  - **Segmentación de red**: VLANs separadas para OT (Operational Technology) y IT.
  - **Microsegmentación**: políticas de firewall por aplicación y usuario.
- **Implementación**:
  - API Gateway con autenticación obligatoria.
  - JWT en cada llamada interna entre microservicios.
  - Validación de certificados en comunicación PLC ←→ Gateway.

---

## 📱 Mobile & Web Integration

- **Login en app móvil/web**: mismo flujo (email + MFA).
- **Biometría**: Touch ID / Face ID para re-autenticación rápida (no para MFA inicial).
- **“Modo invitado”**: solo para dashboards públicos (sin login, sin datos sensibles).

---

## 📊 Identity Dashboard (Para Administradores de Seguridad)

- **Vista en tiempo real**:
  - Intentos de login fallidos.
  - Sesiones activas por usuario/rol.
  - Acciones críticas ejecutadas (con MFA).
  - Alertas de comportamiento anómalo (ej: login a las 3am desde país extranjero).
- **Reportes**:
  - Usuarios con permisos excesivos.
  - Sesiones no revocadas de empleados dados de baja.
  - Uso de MFA por departamento.

---

## 🔐 Seguridad del Módulo Identity (Sí, ¡hasta el módulo de seguridad necesita seguridad!)

- **Encriptación**: Todo en tránsito (TLS 1.3) y en reposo (AES-256).
- **Hardening**: Servidor de auth aislado, sin acceso SSH público.
- **Rate limiting**: Máx. 5 intentos de login/min → bloqueo temporal.
- **Honeytokens**: Credenciales trampa para detectar intentos de intrusión.

---

## 📈 Métricas Clave

- `identity_login_attempts_per_hour`
- `identity_mfa_usage_rate`
- `identity_failed_logins`
- `identity_sessions_active`
- `identity_policy_denials`

---

## 🧪 Ejemplo de Flujo: Técnico Ejecuta Comando Crítico

1. Carlos (técnico) → intenta detener Motor 7 desde app móvil.
2. API Gateway → intercepta petición → valida JWT (válido, rol=technician).
3. Policy Engine → verifica: ¿Carlos tiene permiso para DETENER máquinas en Línea 3? → Sí.
4. ¿Acción requiere MFA? → Sí (por ser “emergency_stop”).
5. Sistema → envía push a app de autenticación de Carlos: “¿Confirmar detención de Motor 7?”.
6. Carlos → aprueba en app → sistema recibe token MFA.
7. Policy Engine → permite acción → Core Engine ejecuta comando.
8. Audit Log → registra:  
   `{ user: Carlos, action: emergency_stop, resource: machine_7, mfa_used: true, ip: 192.168.1.45, success: true }`

⏱️ **Tiempo total: < 20 segundos — con seguridad industrial de grado militar.**

---

## 📁 Estructura de Código Recomendada

```
backend/
├── identity/
│   ├── __init__.py
│   ├── auth_engine.py
│   ├── permission_evaluator.py
│   ├── session_manager.py
│   ├── policy_decision.py
│   └── audit_logger.py
├── models/
│   └── identity_models.py  # Pydantic models
└── database/
    └── db_identity.py      # Acceso a user_permissions, access_audit_log

# Integración con Vault (configuración separada)
vault/
└── policies/
    ├── core-engine-policy.hcl
    └── plc-credentials-policy.hcl
```

---

## 🧭 ¿Cómo empezar a desarrollar?

```bash
# 1. Instala dependencias
pip install python-jose[cryptography] passlib bcrypt python-multipart

# 2. Crea tablas de permisos y auditoría
CREATE TABLE user_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    machine_id INTEGER REFERENCES assets(id),
    action VARCHAR(50) NOT NULL,
    zone VARCHAR(100),
    valid_during_shift BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE access_audit_log (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource VARCHAR(200),
    ip_address VARCHAR(45),
    user_agent TEXT,
    success BOOLEAN NOT NULL,
    mfa_used BOOLEAN DEFAULT FALSE,
    session_id VARCHAR(100),
    metadata JSONB
);

# 3. Levanta el módulo
uvicorn identity.main:app --reload --port 8007

# 4. Prueba login (simulado)
curl -X POST http://localhost:8007/login \
  -H "Content-Type: application/json" \
  -d '{"email": "carlos@planta.com", "password": "secreto123"}'

# 5. Verifica logs en http://localhost:8007/audit
```

---

## 📌 Decisiones Clave

- **MFA obligatorio para acciones críticas** → no negociable.
- **Permisos granulares por máquina/acción** → evita privilegios excesivos.
- **Auditoría inmutable** → cumplimiento + mejora continua.
- **Zero Trust desde el inicio** → no “seguridad perimetral”.
- **Nada de secretos en código** → todo en Vault.

---

> “En una fábrica digital, el peor fallo no es una máquina parada.  
> Es un intruso en el sistema, un comando malicioso, o un secreto industrial robado.  
> Este módulo es el guardián que nunca duerme.”

➡️ **¡FELICITACIONES! Has completado todos los módulos principales.  
Ahora toca el documento maestro: `02-arquitectura-global.md` (que ya hicimos) y luego el `README.md` raíz.**
```

---

## ✅ ACCIONES INMEDIATAS

1. Guarda este contenido como `identity.md` en `03-modulos/`.
2. Ejecuta el script SQL en tu PostgreSQL.
3. Crea la carpeta `backend/identity/` y los archivos `.py` vacíos.
4. ¡TOMA UN DESCANSO Y CELEBRA! 🎉 Acabas de definir el sistema de seguridad industrial que protegerá tu fábrica digital.

---
