Ahora toca el módulo que **convierte las alertas de IA en acciones reales, tangibles, en el piso de planta** — el **Maintenance Module**.

Este es el puente entre el mundo digital (predicciones, modelos, datos) y el mundo físico (técnicos, llaves, repuestos, grasa y tornillos).

---

## 📄 `03-modulos/maintenance.md` — LISTO PARA COPIAR Y PEGAR

```markdown
# 🛠️ Módulo: Maintenance — El Sistema de Mantenimiento Industrial 5.0

> **Gestión integral de mantenimiento: correctivo, preventivo, predictivo y proactivo — con IA, inventario inteligente, asignación automática y mejora continua. Todo integrado, todo rastreable, todo optimizado.**

---

## 🎯 Propósito

El **Maintenance Module** es el subsistema responsable de:

- **Convertir alertas de IA** en órdenes de trabajo reales (OTs).
- **Gestionar todo el ciclo de vida del mantenimiento**: desde la detección hasta el cierre.
- **Administrar inventario de repuestos** con niveles mínimos inteligentes y sugerencias de compra.
- **Asignar técnicos automáticamente** según habilidad, ubicación y carga de trabajo.
- **Medir y mejorar KPIs industriales**: MTTR, MTBF, OEE, costos de parada.
- **Generar mejoras continuas** con análisis de root cause y lecciones aprendidas.

> No es un CMMS tradicional. Es un sistema autónomo, predictivo y centrado en evitar que la máquina falle — no solo en arreglarla.

---

## 🧩 Componentes Internos

```
[ AI Orchestrator ] → (alertas) → [ Work Order Generator ]
                                      ↓
                             [ Technician Assigner ]
                                      ↓
                          [ Inventory & Spare Parts Manager ]
                                      ↓
                           [ Mobile Work Order Dispatcher ]
                                      ↓
                        [ Closure & Continuous Improvement ]
```

---

## 📥 Entradas Clave

- **Alertas de IA** (desde `ai-orchestrator`):  
  ```json
  { "machine_id": 7, "risk_level": "HIGH", "recommended_action": "Revisar rodamientos" }
  ```
- **Calendarios preventivos** (configurados por supervisor).
- **Solicitudes manuales** (operario reporta fallo vía app móvil).
- **Inventario actual** (niveles de repuestos, ubicaciones).
- **Disponibilidad de técnicos** (turnos, habilidades, ubicación en planta).

---

## 📝 Work Order Generator (Generador de Órdenes de Trabajo)

- **Función**: Convierte alertas o solicitudes en OTs estructuradas.
- **Campos de una OT**:
  - ID único
  - Máquina afectada
  - Prioridad (Baja, Media, Alta, Crítica)
  - Descripción + acción recomendada
  - Checklist de pasos (generado por IA o manual)
  - Fotos/videos de referencia (si aplica)
  - Fecha límite (basada en riesgo)
  - Estado (Pendiente, En Progreso, En Espera, Completado, Cancelado)

> ✅ Las OTs se guardan en tabla `maintenance_orders` (PostgreSQL).

---

## 👷 Technician Assigner (Asignador Inteligente de Técnicos)

- **Función**: Asigna automáticamente la OT al técnico más adecuado.
- **Criterios de asignación**:
  - Habilidad requerida (ej: “rodamientos”, “hidráulica”).
  - Ubicación actual (geolocalización por BLE/UWB o último check-in).
  - Carga de trabajo actual (OTs abiertas).
  - Turno activo.
- **Fallback**: Si no hay técnico disponible, notifica al supervisor.

> 📱 **Notificación push**: El técnico recibe la OT en su app móvil con mapa de ubicación de la máquina.

---

## 📦 Inventory & Spare Parts Manager (Gestor de Inventario Inteligente)

- **Función**: Gestiona repuestos, sugiere compras, evita faltantes.
- **Tabla `spare_parts`**:
  ```sql
  CREATE TABLE spare_parts (
      id SERIAL PRIMARY KEY,
      name VARCHAR(200) NOT NULL,
      code VARCHAR(50) UNIQUE,
      category VARCHAR(100), -- "rodamientos", "sellos", "motores"
      stock_level INTEGER NOT NULL,
      min_level INTEGER NOT NULL, -- nivel mínimo automático (ajustado por IA)
      location TEXT, -- "Almacén A, Estante 3, Caja 7"
      last_used TIMESTAMPTZ,
      avg_monthly_usage INTEGER
  );
  ```
- **IA de inventario**:
  - Predice consumo mensual → ajusta `min_level`.
  - Sugiere compra si stock < min_level → genera orden de compra.
  - Alerta si repuesto crítico está por agotarse.

> 🏷️ **Integración con QR/RFID**: Técnico escanea repuesto → sistema registra uso automático → actualiza inventario.

---

## 📱 Mobile Work Order Dispatcher (App Móvil para Técnicos)

- **Función**: Interfaz principal para técnicos en piso de planta.
- **Características clave**:
  - Lista de OTs asignadas (con prioridad y tiempo restante).
  - Escaneo QR de máquina → abre OT + manual + historial.
  - Checklist interactivo (marca pasos completados).
  - Subida de fotos/videos de falla o reparación.
  - Modo OFFLINE: sincroniza al reconectar.
  - Reconocimiento de voz: “OT completada, comentarios: rodamiento desgastado, reemplazado.”
  - Geolocalización: registra dónde se realizó la OT.

> ✅ Desarrollado en **React Native** — comparte lógica con app web.

---

## 🔄 Closure & Continuous Improvement (Cierre y Mejora Continua)

- **Cierre de OT**:
  - Técnico marca como “Completado”.
  - Sube evidencias (fotos, notas).
  - Sistema registra tiempo real vs estimado.
- **Análisis post-OT**:
  - Root Cause sugerido por IA (basado en descripción y fotos).
  - Lección aprendida → se agrega a base de conocimiento.
  - Actualiza modelo predictivo: “esta vibración + este sonido = fallo en 48h”.
- **KPIs automáticos**:
  - MTTR (Tiempo Medio de Reparación)
  - MTBF (Tiempo Medio Entre Fallas)
  - Costo de parada por máquina

---

## 📊 Tablero de Mantenimiento (Para Supervisores)

- **Vista en tiempo real**:
  - OTs abiertas por prioridad.
  - Técnicos asignados vs libres.
  - Nivel de inventario crítico.
  - MTTR semanal.
- **Alertas visuales**:
  - OTs vencidas.
  - Repuestos por agotarse.
  - Máquinas con frecuencia de fallas anormal.

---

## 🔐 Seguridad y Auditoría

- **RBAC estricto**:
  - Técnico: solo ver y cerrar sus OTs.
  - Supervisor: asignar, reasignar, cerrar cualquier OT.
  - Planner: crear calendarios preventivos.
- **Auditoría completa**:
  - Quién creó, asignó, modificó, cerró cada OT.
  - Cuándo se usó cada repuesto.
  - Fotos y notas asociadas.

---

## 📈 Métricas Clave

- `maintenance_ot_open_count`
- `maintenance_mttr_hours`
- `maintenance_mtbf_hours`
- `maintenance_spare_parts_stockout_events`
- `maintenance_ai_recommendation_accuracy`

---

## 🧪 Ejemplo de Flujo: Alerta de IA → OT Cerrada

1. IA detecta riesgo alto en Motor 7 → genera alerta.
2. Work Order Generator → crea OT #487: “Revisar rodamientos. Prioridad: Alta. Deadline: 48h.”
3. Technician Assigner → asigna a Carlos (experto en motores, ubicado a 20m, 2 OTs abiertas).
4. Carlos recibe push en su móvil → abre OT → escanea QR del motor.
5. Sigue checklist → reemplaza rodamiento → escanea código del repuesto → inventario -1.
6. Sube foto del rodamiento dañado → escribe: “Desgaste anormal. Revisar alineación.”
7. Marca OT como completada → sistema registra MTTR = 2.3h.
8. IA analiza foto y nota → actualiza modelo: “vibración > 4.5mm/s + ruido agudo = fallo rodamiento en 36h ±10%”.
9. Supervisor ve en dashboard: MTTR de motores bajó de 4.1h a 2.3h este mes.

⏱️ **Tiempo total desde alerta hasta mejora del modelo: < 3 días.**

---

## 📁 Estructura de Código Recomendada

```
backend/
├── maintenance/
│   ├── __init__.py
│   ├── work_order_generator.py
│   ├── technician_assigner.py
│   ├── inventory_manager.py
│   ├── mobile_dispatcher.py
│   └── continuous_improvement.py
├── models/
│   └── maintenance_models.py  # Pydantic models
└── database/
    └── db_maintenance.py      # Acceso a maintenance_orders, spare_parts

mobile_app/
└── src/
    └── screens/
        ├── MaintenanceOTList.js
        ├── MaintenanceOTDetail.js
        ├── SparePartScanner.js
        └── VoiceNoteRecorder.js
```

---

## 🧭 ¿Cómo empezar a desarrollar?

```bash
# 1. Crea las tablas en PostgreSQL (ver script abajo)
# 2. Instala dependencias backend
pip install geopy  # para asignación por ubicación

# 3. Levanta el módulo de mantenimiento
uvicorn maintenance.main:app --reload --port 8002

# 4. Simula una alerta de IA
curl -X POST http://localhost:8002/maintenance/alert \
  -H "Content-Type: application/json" \
  -d '{"machine_id": 7, "risk_level": "HIGH", "action": "Revisar rodamientos"}'

# 5. Verifica OT generada en http://localhost:8002/maintenance/orders
```

### 📜 Script SQL Inicial (Ejecutar en PostgreSQL)

```sql
-- Tabla de órdenes de trabajo
CREATE TABLE maintenance_orders (
    id SERIAL PRIMARY KEY,
    machine_id INTEGER NOT NULL REFERENCES machines(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(10) NOT NULL, -- 'low', 'medium', 'high', 'critical'
    status VARCHAR(20) NOT NULL DEFAULT 'pending', -- 'pending', 'in_progress', 'on_hold', 'completed', 'cancelled'
    assigned_to INTEGER REFERENCES users(id), -- técnico asignado
    due_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    checklist JSONB, -- pasos a seguir
    evidence JSONB   -- fotos, notas, voz
);

-- Tabla de repuestos
CREATE TABLE spare_parts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    category VARCHAR(100),
    stock_level INTEGER NOT NULL DEFAULT 0,
    min_level INTEGER NOT NULL DEFAULT 5,
    location TEXT,
    last_used TIMESTAMPTZ,
    avg_monthly_usage INTEGER DEFAULT 0
);

-- Índices
CREATE INDEX idx_maintenance_orders_status ON maintenance_orders(status);
CREATE INDEX idx_maintenance_orders_due_date ON maintenance_orders(due_date);
CREATE INDEX idx_spare_parts_stock ON spare_parts(stock_level);
```

---

## 📌 Decisiones Clave

- **OTs generadas automáticamente por IA** → reduce tiempo de reacción.
- **Asignación inteligente de técnicos** → optimiza recursos humanos.
- **Inventario con IA** → nunca más “se acabó el repuesto crítico”.
- **App móvil offline-first** → funciona en zonas sin Wi-Fi.
- **Mejora continua embebida** → cada reparación hace al sistema más inteligente.

---

> “El mejor mantenimiento no es el más rápido. Es el que nunca fue necesario.  
> Pero cuando es necesario, debe ser impecable, rastreable y que deje a la máquina mejor que antes.”

➡️ **Siguiente paso recomendado: definir el módulo de activos (`assets.md`) — catálogo inteligente de máquinas, sensores, líneas, y su salud en tiempo real.**
```

---

## ✅ ACCIONES INMEDIATAS

1. Guarda este contenido como `maintenance.md` en `03-modulos/`.
2. Ejecuta el script SQL en tu PostgreSQL.
3. Crea la carpeta `backend/maintenance/` y los archivos `.py` vacíos.
4. ¡Celebra! Acabas de definir el sistema que mantendrá tu fábrica funcionando sin sorpresas.
