Ahora toca el módulo que **cataloga, monitorea y da vida digital a cada máquina, sensor, línea y activo de tu planta** — el **Assets Module**.

Este es el “pasaporte digital” de cada pieza de tu fábrica. Sin él, no hay control, no hay trazabilidad, no hay gemelo digital.

---

## 📄 `03-modulos/assets.md` — LISTO PARA COPIAR Y PEGAR

```markdown
# 🏭 Módulo: Assets — El Catálogo Inteligente de la Planta

> **Registro unificado, en tiempo real, de todos los activos industriales: máquinas, sensores, líneas, robots — con su estado, historial, gemelo digital, y salud predictiva. La base de todo control, mantenimiento y optimización.**

---

## 🎯 Propósito

El **Assets Module** es el subsistema responsable de:

- **Catalogar todos los activos físicos** de la planta (máquinas, sensores, actuadores, líneas, robots, herramientas).
- **Monitorear su estado en tiempo real** (operativo, parado, en mantenimiento, falla).
- **Almacenar su historial completo** (mantenimientos, fallos, modificaciones, upgrades).
- **Asociar sensores y actuadores** a cada máquina.
- **Exponer su “gemelo digital ligero”** (modelo 3D, parámetros, límites, KPIs).
- **Calcular su “salud predictiva”** (basada en IA y mantenimiento).
- **Integrarse con todos los módulos**: Core Engine, IA, Mantenimiento, Reporting.

> Sin este módulo, los datos son ruido. Con él, cada dato tiene dueño, contexto y propósito.

---

## 🧩 Componentes Internos

```
[ Core Engine ] → (datos de sensores) → [ Asset State Monitor ]
[ Maintenance ] → (OTs, repuestos)     → [ Asset History Logger ]
[ AI Orchestrator ] → (predicciones)   → [ Asset Health Calculator ]
                                          ↓
                                 [ Digital Twin Registry ]
                                          ↓
                               [ Asset Catalog API + UI ]
```

---

## 📥 Entradas Clave

- **Datos de sensores** (desde Core Engine): asignados a activos específicos.
- **Eventos de estado**: arranque, parada, alarma, error.
- **Órdenes de trabajo** (desde Maintenance): asociadas a activos.
- **Predicciones de IA** (desde AI Orchestrator): salud, riesgo, vida útil restante.
- **Metadatos manuales**: fotos, manuales, planos, especificaciones técnicas.

---

## 🗃️ Asset Catalog (Catálogo de Activos)

### Tabla `assets` en PostgreSQL

```sql
CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,           -- "Motor Principal Línea 3"
    code VARCHAR(50) UNIQUE NOT NULL,     -- "MTR-L3-001"
    type VARCHAR(50) NOT NULL,            -- "motor", "sensor", "plc", "robot", "line"
    category VARCHAR(100),                -- "eléctrico", "mecánico", "neumático"
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    serial_number VARCHAR(100),
    installation_date DATE,
    warranty_expiry DATE,
    location TEXT,                        -- "Línea 3, Estación 2, Zona Norte"
    status VARCHAR(20) DEFAULT 'operativo', -- 'operativo', 'parado', 'mantenimiento', 'falla'
    health_score FLOAT DEFAULT 100.0,     -- 0-100, calculado por IA
    last_health_update TIMESTAMPTZ,
    metadata JSONB,                       -- fotos, manuales, planos, links
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

> ✅ Cada activo tiene un **código único** → usado en todas las integraciones (QR, OTs, sensores).

---

## 🔄 Asset State Monitor (Monitor de Estado en Tiempo Real)

- **Función**: Actualiza el estado del activo en tiempo real.
- **Fuentes**:
  - Sensores (¿está enviando datos? ¿dentro de rangos?).
  - PLCs (bit de “running”, “fault”).
  - Mantenimiento (si tiene OT abierta → estado = “mantenimiento”).
- **Estados posibles**:
  - `operativo` → funcionando normal.
  - `parado` → detenido intencionalmente.
  - `mantenimiento` → OT activa asignada.
  - `falla` → sensor fuera de rango o error PLC.
- **Actualización**: Cada 10s-1min → vía Core Engine.

---

## 📚 Asset History Logger (Registro Histórico)

- **Función**: Guarda todo lo que le pasa a un activo.
- **Tabla `asset_events`**:
  ```sql
  CREATE TABLE asset_events (
      id SERIAL PRIMARY KEY,
      asset_id INTEGER REFERENCES assets(id),
      event_type VARCHAR(50) NOT NULL, -- 'maintenance', 'failure', 'upgrade', 'calibration'
      description TEXT,
      timestamp TIMESTAMPTZ DEFAULT NOW(),
      related_ot_id INTEGER REFERENCES maintenance_orders(id), -- si aplica
      related_sensor_id INTEGER,
      data JSONB -- valores de sensores, fotos, etc.
  );
  ```
- **Ejemplos**:
  - “2025-04-05: Reemplazo de rodamiento (OT #487)”.
  - “2025-04-04: Vibración excedida → alerta IA #203”.
  - “2025-03-20: Calibración de sensor de presión”.

---

## ❤️ Asset Health Calculator (Calculador de Salud Predictiva)

- **Función**: Asigna un “puntaje de salud” (0-100) a cada activo.
- **Fuentes**:
  - Últimas alertas de IA (gravedad, frecuencia).
  - MTBF y MTTR históricos.
  - Días desde último mantenimiento.
  - Desgaste estimado (basado en horas de uso y carga).
- **Fórmula inicial (Fase MVP)**:
  ```
  Salud = 100 
          - (días_sin_mantenimiento * 0.5) 
          - (n_alertas_últimos_30_días * 3) 
          - (MTTR_promedio * 2)
  ```
- **Salida**: Actualiza `health_score` en tabla `assets` → visible en dashboards.

> 📈 En Fase 2: Modelo de ML (Random Forest) que predice vida útil restante.

---

## 🧊 Digital Twin Registry (Registro de Gemelos Digitales)

- **Función**: Asocia a cada activo su representación digital.
- **Campos en `metadata` (JSONB)**:
  ```json
  {
    "digital_twin": {
      "model_3d_url": "https://.../motor_l3.glb",
      "parameters": {
        "max_temp": 90,
        "max_vibration": 5.0,
        "optimal_speed": 1200
      },
      "sensors": ["TEMP_MOTOR", "VIB_MOTOR", "CURRENT"],
      "actuators": ["SPEED_CTRL", "COOLING_VALVE"]
    }
  }
  ```
- **Uso**:
  - Simulador de “qué pasaría si...”.
  - Visualización 3D en dashboard.
  - Entrenamiento de IA en entorno simulado.

---

## 📱 Asset Mobile Interface (Interfaz Móvil para Activos)

- **Función**: Acceso rápido a información de activos desde el piso de planta.
- **Características**:
  - Escaneo QR → abre ficha completa del activo.
  - Vista rápida: estado, salud, última OT, sensores asociados.
  - Botón “Reportar problema” → genera OT inmediata.
  - Historial de eventos (con fotos y notas).
  - Enlace a manual de operación/mantenimiento (PDF o video).

> ✅ Desarrollado en **React Native** — comparte componente `AssetCard` con web.

---

## 🖥️ Asset Web Dashboard (Para Supervisores e Ingenieros)

- **Vista de planta por líneas/zonas**.
- **Fichas de activos con**:
  - Estado actual (color: verde/amarillo/rojo).
  - Salud predictiva (barra 0-100).
  - KPIs clave (MTBF, MTTR, OEE).
  - Últimos eventos.
  - Gráficos de sensores en vivo.
- **Filtros**:
  - Por tipo, categoría, estado, salud.
  - Por línea o zona de planta.

---

## 🔐 Seguridad y Auditoría

- **RBAC por activo**:
  - Operario: ver estado y reportar fallos.
  - Técnico: ver historial y OTs.
  - Ingeniero: editar metadatos y gemelo digital.
- **Auditoría de cambios**:
  - Quién modificó qué y cuándo (trigger en PostgreSQL).

---

## 📈 Métricas Clave

- `assets_total_count`
- `assets_operational_percentage`
- `assets_health_avg_score`
- `assets_with_critical_health_count`
- `asset_events_per_day`

---

## 🧪 Ejemplo de Flujo: Operario Escanea QR de Máquina

1. Operario en piso → escanea QR de “Motor Línea 3” con app móvil.
2. App consulta API → devuelve ficha:
   - Estado: OPERATIVO (verde)
   - Salud: 87/100
   - Última OT: hace 12 días (“Revisión rodamientos”)
   - Sensores: Temp=82°C, Vib=3.1mm/s
   - Manual: [Ver PDF]
3. Operario nota vibración anormal → toca “Reportar Problema”.
4. App genera OT #488 → asignada automáticamente → técnico recibe push.
5. Técnico llega → escanea mismo QR → ve historial → diagnostica → repara.
6. Sistema actualiza salud a 95/100 → registra evento → actualiza KPIs.

⏱️ **Tiempo total desde detección hasta mejora de salud: < 4 horas.**

---

## 📁 Estructura de Código Recomendada

```
backend/
├── assets/
│   ├── __init__.py
│   ├── asset_catalog.py
│   ├── state_monitor.py
│   ├── history_logger.py
│   ├── health_calculator.py
│   └── digital_twin_registry.py
├── models/
│   └── asset_models.py  # Pydantic models
└── database/
    └── db_assets.py      # Acceso a assets, asset_events

mobile_app/
└── src/
    └── screens/
        ├── AssetScanner.js
        ├── AssetDetail.js
        └── AssetHealthChart.js

web_app/
└── src/
    └── components/
        ├── AssetMap.js
        ├── AssetCard.js
        └── AssetHealthGauge.js
```

---

## 🧭 ¿Cómo empezar a desarrollar?

```bash
# 1. Ejecuta el script SQL de arriba en PostgreSQL
# 2. Instala dependencias (si usas geolocalización)
pip install geoalchemy2  # si usas ubicaciones geográficas

# 3. Levanta el módulo de activos
uvicorn assets.main:app --reload --port 8003

# 4. Registra tu primera máquina
curl -X POST http://localhost:8003/assets \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Motor Principal Línea 3",
    "code": "MTR-L3-001",
    "type": "motor",
    "category": "eléctrico",
    "location": "Línea 3, Estación 2",
    "status": "operativo"
  }'

# 5. Verifica en http://localhost:8003/assets/1
```

---

## 📌 Decisiones Clave

- **Código único por activo** → base de toda trazabilidad.
- **Salud predictiva simple al inicio** → evita overengineering.
- **Gemelo digital en metadata (JSONB)** → flexible, sin sobrecarga.
- **App móvil con QR** → adopción instantánea en piso de planta.
- **Integración total** → sin activos, nada funciona.

---

> “Un activo sin ficha digital es como un empleado sin legajo: existe, pero no sabes qué hace, cómo está, ni qué necesita.”

➡️ **Siguiente paso recomendado: definir el módulo de procurement (`procurement.md`) — gestión inteligente de compras, proveedores, repuestos y nuevos proyectos.**
```

---

## ✅ ACCIONES INMEDIATAS

1. Guarda este contenido como `assets.md` en `03-modulos/`.
2. Ejecuta el script SQL en tu PostgreSQL.
3. Crea la carpeta `backend/assets/` y los archivos `.py` vacíos.
4. ¡Respira! Acabas de digitalizar el alma de tu fábrica — cada máquina ahora tiene identidad, historia y salud.
