Este no es un simple “envío de emails”. Es un **sistema multimodal, en tiempo real, con prioridades, confirmaciones y escalabilidad industrial** — porque en una fábrica, **una alerta no vista es una máquina parada, un riesgo de seguridad, o un cliente insatisfecho**.

---

## 📄 `03-modulos/notifications.md` — LISTO PARA COPIAR Y PEGAR

```markdown
# 🔔 Módulo: Notifications — Sistema Multimodal de Alertas Industriales

> **Motor de notificaciones en tiempo real que garantiza que cada alerta, evento crítico o acción requerida llegue al destinatario correcto, por el canal correcto, en el momento correcto — con confirmación, escalado automático y soporte para dispositivos industriales (sirenas, luces, tableros LED).**

---

## 🎯 Propósito

El **Notifications Module** es el subsistema responsable de:

- **Recibir eventos y alertas** de todos los módulos (Core, IA, Mantenimiento, Reporting).
- **Clasificarlos por criticidad** (Informativo, Advertencia, Crítico, Emergencia).
- **Enrutarlos a los destinatarios correctos** según rol, ubicación y disponibilidad.
- **Enviarlos por múltiples canales**: app móvil (push), email, SMS, sirenas, luces, tableros LED, WebSocket.
- **Exigir confirmación de lectura/acción** para alertas críticas.
- **Escalar automáticamente** si no hay respuesta en X minutos.
- **Registrar auditoría completa** de envíos, confirmaciones y tiempos de respuesta.

> En una fábra 24/7, **una alerta no vista es una falla no atendida. Este módulo asegura que eso nunca pase.**

---

## 🧩 Componentes Internos

```
[ AI Orchestrator ] → (alertas)       → [ Notification Router ]
[ Maintenance ] → (OT urgente)        → [ Channel Dispatcher ]
[ Core Engine ] → (parada de línea)   → [ Escalation Engine ]
[ Reporting ] → (KPI crítico)         → [ Confirmation Tracker ]
                                         ↓
                  ┌─────────────────────┴─────────────────────┐
                  ▼                     ▼                     ▼
           [ Mobile Push ]       [ Email / SMS ]     [ Industrial Devices ]
                  ▼                     ▼                     ▼
           [ App Móvil ]         [ Outlook / Tel ]     [ Sirenas / Luces / LED ]
```

---

## 📥 Entradas Clave

Cualquier módulo puede enviar una notificación con este formato estandarizado:

```json
{
  "event_id": "evt_20250405_001",
  "source_module": "ai-orchestrator",
  "event_type": "machine_failure_prediction",
  "severity": "CRITICAL", // INFO, WARNING, CRITICAL, EMERGENCY
  "title": "Falla inminente en Motor Línea 3",
  "message": "Riesgo alto (92%) de fallo en próximas 48h. Revisar rodamientos.",
  "target_roles": ["technician", "maintenance_supervisor"],
  "target_machines": [7],
  "target_locations": ["Line 3"],
  "required_ack": true, // ¿Requiere confirmación?
  "escalation_time": 15, // minutos sin ack → escala
  "metadata": {
    "machine_id": 7,
    "predicted_failure_time": "2025-04-07T10:00:00Z",
    "recommended_action": "Reemplazar rodamiento 6205"
  }
}
```

---

## 🧭 Notification Router (Enrutador Inteligente)

- **Función**: Decide **a quién** y **por dónde** enviar la notificación.
- **Reglas de enrutamiento**:
  - Por rol: “technician”, “supervisor”, “manager”.
  - Por máquina/ubicación: solo técnicos asignados a Línea 3.
  - Por disponibilidad: si el técnico está en turno (integración con RRHH).
  - Por preferencia de usuario: algunos prefieren SMS, otros push.
- **Salida**: Lista de destinatarios + canales prioritarios.

---

## 📱 Channel Dispatcher (Despachador Multicanal)

- **Función**: Envía la notificación por todos los canales configurados.
- **Canales soportados**:

| Canal               | Tecnología / Integración          | Uso típico                          |
|---------------------|-----------------------------------|-------------------------------------|
| **Mobile Push**     | Firebase Cloud Messaging (FCM)    | Alertas operativas, OTs             |
| **Email**           | SMTP (SendGrid, AWS SES)          | Reportes, resúmenes, alertas no urgentes |
| **SMS**             | Twilio / Vonage API               | Alertas críticas fuera de turno     |
| **WebSocket**       | FastAPI WebSockets                | Dashboards en tiempo real           |
| **Industrial Devices** | MQTT → PLC → Sirenas/Luces/LED  | Alertas de planta (visuales/sonoras)|
| **Microsoft Teams** | Webhook                           | Equipos de soporte                  |

> ✅ Cada usuario configura sus canales preferidos en su perfil.

---

## 🆘 Escalation Engine (Motor de Escalamiento)

- **Función**: Si una alerta crítica no es confirmada, ¡se escala!
- **Flujo**:
  1. Minuto 0: Notificación enviada a Técnico A.
  2. Minuto 15: Sin confirmación → notifica a Supervisor de Mantenimiento.
  3. Minuto 30: Sin confirmación → notifica a Gerente de Planta + sirena en Línea 3.
  4. Minuto 45: Sin confirmación → notifica a Director de Operaciones + SMS a celular.
- **Personalizable por tipo de alerta**.

---

## ✅ Confirmation Tracker (Rastreador de Confirmaciones)

- **Función**: Registra quién confirmó, cuándo, y desde dónde.
- **Acciones de confirmación**:
  - “Visto” → solo acuse de recibo.
  - “En camino” → técnico se dirige a la máquina.
  - “Resuelto” → problema solucionado.
  - “Falso positivo” → reportar error de IA.
- **Tabla `notifications_audit`**:
  ```sql
  CREATE TABLE notifications_audit (
      id SERIAL PRIMARY KEY,
      event_id VARCHAR(50) NOT NULL,
      user_id INTEGER REFERENCES users(id),
      channel VARCHAR(20) NOT NULL, -- 'push', 'email', 'sms', 'siren'
      sent_at TIMESTAMPTZ NOT NULL,
      acknowledged_at TIMESTAMPTZ,
      action_taken VARCHAR(50), -- 'seen', 'on_way', 'resolved', 'false_positive'
      escalation_level INTEGER DEFAULT 0
  );
  ```

---

## 🚨 Industrial Devices Integration (Integración con Dispositivos Físicos)

- **Función**: Activar sirenas, luces estroboscópicas, o tableros LED en planta.
- **Protocolo**: MQTT → Gateway → PLC → Salidas digitales.
- **Ejemplo**:
  - Alerta “EMERGENCIA” → activa sirena + luz roja en zona afectada.
  - Alerta “CRÍTICA” → muestra mensaje en tablero LED: “MOTOR 7 - REVISAR YA”.
- **Confirmación física**: Algunos tableros tienen botón “ACK” → envía confirmación vía MQTT.

---

## 📱 Mobile App Integration (App Móvil)

- **Notificaciones push** con:
  - Título, mensaje, prioridad (sonido diferente por severidad).
  - Acciones rápidas: “Ver OT”, “Navegar a máquina”, “Confirmar”.
  - Modo “No molestar” configurable (ej: solo EMERGENCIA).
- **Offline**: Si no hay red, la notificación se guarda y sincroniza luego.

---

## 📊 Notification Dashboard (Para Supervisores)

- **Vista en tiempo real**:
  - Alertas pendientes de confirmación.
  - Tiempo promedio de respuesta por técnico.
  - Tasa de falsos positivos de IA.
  - Canales más efectivos por tipo de alerta.
- **Alertas de sistema**:
  - “Técnico Carlos no confirma alertas críticas → revisar disponibilidad.”
  - “Canal SMS con 20% de fallas → revisar proveedor.”

---

## 🔐 Seguridad y Auditoría

- **RBAC**: Solo roles autorizados reciben ciertas alertas (ej: solo gerentes ven alertas de costo).
- **Encriptación**: Notificaciones en tránsito (TLS) y en reposo (para mensajes en cola).
- **Auditoría completa**: Quién envió, a quién, por qué canal, cuándo se confirmó.
- **Rate limiting**: Evita spam de notificaciones (máx. 5 alertas/min por usuario en modo CRÍTICO).

---

## 📈 Métricas Clave

- `notifications_sent_per_hour`
- `notifications_ack_rate`
- `avg_ack_time_seconds`
- `escalations_triggered`
- `false_positive_rate`

---

## 🧪 Ejemplo de Flujo: Alerta Crítica → Confirmada en 3 Minutos

1. IA detecta riesgo crítico en Motor 7 → envía alerta al Notifications Module.
2. Router → asigna a Técnico Carlos (especialista en motores, en turno, en Línea 3).
3. Channel Dispatcher → envía:
   - Push a app móvil de Carlos (sonido de alerta crítica).
   - Mensaje en tablero LED de Línea 3: “MOTOR 7 - RIESGO ALTO”.
4. Carlos recibe push → toca “En camino” → sistema registra ack en 47 segundos.
5. Tablero LED cambia a “EN ATENCIÓN - CARLOS”.
6. Supervisor ve en dashboard: “Alerta crítica atendida en 47s. ¡Excelente!”.
7. Si Carlos no hubiera respondido en 15 min → se escala al supervisor + sirena.

⏱️ **Tiempo total desde alerta hasta acción: < 3 minutos.**

---

## 📁 Estructura de Código Recomendada

```
backend/
├── notifications/
│   ├── __init__.py
│   ├── notification_router.py
│   ├── channel_dispatcher.py
│   ├── escalation_engine.py
│   ├── confirmation_tracker.py
│   └── industrial_devices.py
├── models/
│   └── notification_models.py  # Pydantic models
└── database/
    └── db_notifications.py     # Acceso a notifications_audit

mobile_app/
└── src/
    └── components/
        ├── CriticalAlertModal.js
        └── NotificationHistory.js
```

---

## 🧭 ¿Cómo empezar a desarrollar?

```bash
# 1. Instala dependencias
pip install firebase-admin twilio paho-mqtt  # para push, SMS, MQTT

# 2. Crea tabla de auditoría
CREATE TABLE notifications_audit (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(50) NOT NULL,
    user_id INTEGER REFERENCES users(id),
    channel VARCHAR(20) NOT NULL,
    sent_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    acknowledged_at TIMESTAMPTZ,
    action_taken VARCHAR(50),
    escalation_level INTEGER DEFAULT 0
);

# 3. Levanta el módulo
uvicorn notifications.main:app --reload --port 8006

# 4. Simula una alerta crítica
curl -X POST http://localhost:8006/notify \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_test_001",
    "source_module": "test",
    "event_type": "test_alert",
    "severity": "CRITICAL",
    "title": "Prueba de Alerta Crítica",
    "message": "Esto es una prueba. Por favor, confirma.",
    "target_roles": ["technician"],
    "required_ack": true,
    "escalation_time": 5
  }'

# 5. Verifica en http://localhost:8006/notifications/audit
```

---

## 📌 Decisiones Clave

- **Formato estandarizado de eventos** → cualquier módulo puede alertar.
- **Escalamiento automático** → nadie queda fuera de la cadena de respuesta.
- **Confirmación obligatoria** → responsabilidad clara.
- **Integración con dispositivos físicos** → alertas que se ven y se oyen en planta.
- **Auditoría total** → mejora continua del sistema de alertas.

---

> “Una alerta no confirmada es una responsabilidad no asumida.  
> Una alerta no enviada es un sistema fallido.  
> Este módulo asegura que ambas cosas nunca ocurran.”

➡️ **Siguiente paso recomendado: definir el módulo de identidad (`identity.md`) — autenticación, autorización, MFA, SSO, y gestión de roles industriales con Zero Trust.**
```

---

## ✅ ACCIONES INMEDIATAS

1. Guarda este contenido como `notifications.md` en `03-modulos/`.
2. Ejecuta el script SQL en tu PostgreSQL.
3. Crea la carpeta `backend/notifications/` y los archivos `.py` vacíos.
4. ¡Celebra! Acabas de construir el sistema que **nunca dejará que una alerta crítica pase desapercibida**.

---
