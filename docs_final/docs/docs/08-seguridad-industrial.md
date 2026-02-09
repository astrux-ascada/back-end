
# 📄 5. `08-seguridad-industrial.md` — TU FORTALEZA DIGITAL

```markdown
# 🔐 Seguridad Industrial — Políticas y Arquitectura Zero Trust

> **Cómo protegemos secretos industriales, datos de producción y acceso a máquinas críticas — con Zero Trust, MFA, encriptación total y auditoría inmutable.**

---

## 🛡️ Principios Fundamentales

1. **Nunca confiar, siempre verificar** (Zero Trust).
2. **Mínimo privilegio**: solo lo necesario, solo cuando es necesario.
3. **Defensa en profundidad**: múltiples capas de seguridad.
4. **Auditoría total**: todo se loggea, nada se borra.
5. **On-Premise Core**: datos críticos nunca salen de la planta.

---

## 🔑 Autenticación y Autorización

- **MFA Obligatorio** para:
  - Login de usuarios.
  - Acciones críticas (detener máquina, cambiar parámetros).
  - Acceso a dashboards ejecutivos.
- **Métodos Soportados**:
  - App Authenticator (Google/Microsoft).
  - Llave física (FIDO2/WebAuthn).
  - SMS (solo si otros fallan).
- **RBAC Granular**:
  - Por máquina, acción, zona, turno.
  - Ej: “Técnico Carlos → solo controlar Línea 3 en su turno”.

---

## 🔐 Encriptación

| Capa               | Tecnología           | Observaciones                          |
|--------------------|----------------------|----------------------------------------|
| En tránsito        | TLS 1.3              | Entre todas las capas (web, móvil, APIs, PLCs). |
| En reposo          | AES-256              | Discos (LUKS), backups, secretos en Vault. |
| Base de datos      | PostgreSQL pgcrypto  | Datos sensibles cifrados a nivel de columna. |

---

## 🌐 Segmentación de Red

- **VLAN OT (Operational Technology)**: Solo PLCs, sensores, gateways.
- **VLAN IT**: Servidores, desarrollo, administración.
- **Firewall Industrial**: Entre VLANs → solo puertos necesarios.
- **Air-Gapped Opcional**: Para zonas ultra-críticas.

---

## 📜 Auditoría y Cumplimiento

- **Registro Inmutable**: Tabla `access_audit_log` → nunca se borra.
- **Retención**: 10 años (cumplimiento ISO, IEC).
- **Alertas en tiempo real**:
  - Login desde IP sospechosa.
  - Múltiples fallos de MFA.
  - Acceso a máquina fuera de turno.
- **Reportes automáticos**:
  - Usuarios con permisos excesivos.
  - Sesiones no cerradas.

---

## 🚨 Respuesta a Incidentes

- **Modo “Solo Lectura”**: Si se detecta ataque → bloquea todos los comandos.
- **Modo “Pánico”**: Botón físico → detiene toda la planta + activa protocolo.
- **Backup Diario**: Cifrado, fuera de sitio, con prueba de restauración mensual.
- **Disaster Recovery**: Réplica en sitio secundario → activación en < 1h.

---

## 📊 Cumplimiento Normativo

| Norma               | Cobertura                              |
|---------------------|----------------------------------------|
| **ISO 27001**       | Gestión de seguridad de la información |
| **IEC 62443**       | Seguridad en sistemas de control industrial |
| **ISO 55000**       | Gestión de activos                     |
| **GDPR/LOPD**       | Protección de datos personales         |


## 🧭 Próximos Pasos

1. Implementar MFA en login (Fase 1).
2. Configurar VLANs y firewall (Fase 1).
3. Activar auditoría inmutable (Fase 1).
4. Realizar primer test de penetración (Fase 2).

> “En una fábrica digital, la seguridad no es un departamento. Es la cultura. Y este documento es su constitución.”
```
