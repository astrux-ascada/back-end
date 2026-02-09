---

## 📄 `03-modulos/digital-twin.md` — LISTO PARA COPIAR Y PEGAR

```markdown
# 🧊 Módulo: Digital Twin — Simulador y Gemelo Digital Industrial

> **Motor de simulación 3D y física que replica tu planta en tiempo real — para predecir el impacto de cambios, entrenar IA, capacitar operarios y evitar errores costosos ANTES de tocar la máquina real.**

---

## 🎯 Propósito

El **Digital Twin Module** es el subsistema responsable de:

- **Crear y mantener un gemelo digital** de máquinas, líneas o planta completa.
- **Simular escenarios “qué pasaría si…”** (ej: “¿qué pasa si aumento la velocidad un 15%?”).
- **Entrenar modelos de IA** en entorno simulado (sin riesgo para la planta real).
- **Capacitar operarios y técnicos** en entorno virtual (modo entrenamiento).
- **Visualizar estado de la planta** en 3D (opcional, para centros de control avanzados).
- **Integrarse con IA, Assets y Core Engine** para mantener sincronía con el mundo real.

> No es un videojuego. Es un **laboratorio digital donde se prueban decisiones antes de aplicarlas — salvando costos, tiempo y máquinas.**

---

## 🧩 Componentes Internos

```
[ Assets ] → (metadatos, sensores) → [ Twin Model Builder ]
[ Core Engine ] → (datos en vivo)   → [ Real-Time Sync Engine ]
[ AI Orchestrator ] → (acciones)    → [ Simulation Engine ]
                                       ↓
                              [ 3D Visualization Layer ]
                                       ↓
                           [ Training & What-If Interface ]
```

---

## 📥 Entradas Clave

- **Metadatos de activos** (desde `assets.md`): modelo 3D, parámetros físicos, límites.
- **Datos de sensores en vivo** (desde Core Engine): para mantener gemelo sincronizado.
- **Acciones de IA o usuario** (ej: “aumentar velocidad a 1500 rpm”).
- **Condiciones ambientales** (temperatura, humedad, voltaje).

---

## 🏗️ Twin Model Builder (Constructor de Modelos)

- **Función**: Genera el modelo digital de cada activo.
- **Formato del modelo** (almacenado en `assets.metadata`):
  ```json
  {
    "digital_twin": {
      "model_3d_url": "https://models.orquestador.com/motor_l3.glb",
      "physics": {
        "mass_kg": 150,
        "max_temp_c": 90,
        "optimal_speed_rpm": 1200,
        "failure_modes": ["overheat", "imbalance"]
      },
      "sensors": ["TEMP_MOTOR", "VIB_MOTOR", "CURRENT"],
      "actuators": ["SPEED_CTRL", "COOLING_VALVE"]
    }
  }
  ```
- **Herramientas de modelado**:
  - Blender, SolidWorks → exportar a `.glb` (GLTF).
  - Simulación física: NVIDIA PhysX, PyBullet (Python).

---

## 🔄 Real-Time Sync Engine (Motor de Sincronización en Tiempo Real)

- **Función**: Mantiene el gemelo digital sincronizado con la planta real.
- **Frecuencia**: Cada 1-5 segundos (configurable).
- **Mecanismo**:
  - Recibe datos de sensores → actualiza estado del gemelo.
  - Si hay desconexión → usa último valor conocido + predicción simple.
- **Salida**: Estado del gemelo disponible para simulación y visualización.

---

## 🎮 Simulation Engine (Motor de Simulación)

- **Función**: Ejecuta escenarios “qué pasaría si…”.
- **Entrada**: 
  ```json
  {
    "scenario_id": "speed_increase_15",
    "target_asset": "MTR-L3-001",
    "changes": {"SPEED_CTRL": 1500},
    "duration_minutes": 60
  }
  ```
- **Salida**:
  ```json
  {
    "predicted_output": 5750,
    "predicted_scrap_rate": 3.2,
    "predicted_energy_kwh": 120,
    "predicted_wear_level": "HIGH",
    "risk_alerts": ["Temperatura excederá límite en 22 min"]
  }
  ```
- **Tecnología**: Python + NumPy/SciPy + PyBullet (para física).

---

## 🖥️ 3D Visualization Layer (Visualización 3D — Opcional)

- **Función**: Muestra el gemelo digital en 3D en tiempo real.
- **Tecnología**: Three.js (web) o Unity (para centros de control avanzados).
- **Características**:
  - Rotación, zoom, selección de componentes.
  - Overlay de sensores (temperatura en color, vibración en escala).
  - Animación de fallos (ej: motor se pone rojo y humea virtualmente).
- **Requisitos**: Solo para PCs potentes — no para móviles.

---

## 🎓 Training & What-If Interface (Interfaz de Entrenamiento y Simulación)

- **Función**: Permite a usuarios interactuar con el gemelo.
- **Modos**:
  - **What-If**: “Simula aumentar temperatura a 95°C → ¿qué pasa?”.
  - **Training**: “Operario nuevo: practica arrancar la línea sin riesgo”.
  - **AI Training**: “Entrena modelo de RL en gemelo → luego aplica en real”.
- **Integración con app web y móvil** (versión ligera sin 3D).

---

## 🔐 Seguridad

- **Solo roles autorizados** pueden ejecutar simulaciones que afecten parámetros reales.
- **Simulaciones no alteran planta real** → solo lectura de datos, escritura solo en gemelo.
- **Auditoría**: Todas las simulaciones se loggean (quién, cuándo, qué cambió, resultado).

---

## 📈 Métricas Clave

- `digital_twin_sync_latency_ms`
- `simulations_run_per_day`
- `training_sessions_completed`
- `ai_models_trained_in_twin`
- `what_if_scenarios_accepted_rate`

---

## 🧪 Ejemplo de Flujo: Ingeniero Simula Aumento de Velocidad

1. Ingeniero en app web → selecciona “Motor Línea 3” → toca “Simular”.
2. Cambia parámetro: “Velocidad = 1500 rpm” → dura 60 min.
3. Simulation Engine → ejecuta modelo físico → predice:
   - Producción: +15%.
   - Scrap: +2.1%.
   - Temperatura: excede límite en 22 min → riesgo de fallo.
4. Sistema → muestra alerta: “No recomendado. Riesgo alto de sobrecalentamiento.”
5. Ingeniero → decide NO aplicar en planta real → evita fallo costoso.
6. IA → aprende de este escenario → mejora modelo predictivo.

⏱️ **Tiempo total: < 5 minutos — y se evitó una parada de 8 horas.**

---

## 📁 Estructura de Código Recomendada

```
backend/
├── digital_twin/
│   ├── __init__.py
│   ├── model_builder.py
│   ├── sync_engine.py
│   ├── simulation_engine.py
│   └── training_interface.py
├── models/
│   └── digital_twin_models.py
└── database/
    └── db_digital_twin.py  # (aunque usa assets.metadata)

web_app/
└── src/
    └── components/
        ├── DigitalTwinViewer3D.js  # Three.js
        └── WhatIfSimulator.js

mobile_app/
└── src/
    └── screens/
        └── WhatIfScenario.js       # Versión ligera sin 3D
```

---

## 🧭 ¿Cómo empezar a desarrollar?

```bash
# 1. Instala dependencias de simulación
pip install numpy scipy pybullet

# 2. Añade metadatos de gemelo a un activo (ej: Motor 7)
UPDATE assets
SET metadata = metadata || '{"digital_twin": {"model_3d_url": "motor.glb", "physics": {"max_temp_c": 90}}}'::jsonb
WHERE id = 7;

# 3. Levanta el módulo
uvicorn digital_twin.main:app --reload --port 8008

# 4. Ejecuta simulación
curl -X POST http://localhost:8008/digital-twin/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": 7,
    "changes": {"speed": 1500},
    "duration_minutes": 60
  }'

# 5. Verifica resultado en http://localhost:8008/digital-twin/scenarios
```

---

## 📌 Decisiones Clave

- **Gemelo ligero al inicio** → sin 3D, solo simulación de parámetros.
- **Sincronización cada 5s** → balance entre realismo y rendimiento.
- **Entrenamiento de IA en gemelo** → sin riesgos, sin costos.
- **Interfaz “What-If” simple** → valor rápido para ingenieros.
- **3D solo para web** → no forzar en móvil.

---

> “El gemelo digital no reemplaza a la planta. La protege.  
> Permite equivocarse miles de veces en lo virtual… para acertar siempre en lo real.”

➡️ **Siguiente paso: integrar con `ai-orchestrator.md` para entrenamiento autónomo.**
```

---

## ✅ ACCIONES INMEDIATAS

1. Crea el archivo `index.md` dentro de `03-modulos/` → pega el primer contenido.
2. Crea el archivo `digital-twin.md` dentro de `03-modulos/` → pega el segundo contenido.
3. Verifica que todos los enlaces en `index.md` apunten a archivos existentes.
4. ¡Celebra! 🎉 Tu documentación de módulos está **100% completa y profesional**.

---

## 🧾 LISTA DE CHEQUEO FINAL — MÓDULOS

✅ `core-engine.md`  
✅ `ai-orchestrator.md`  
✅ `maintenance.md`  
✅ `assets.md`  
✅ `procurement.md`  
✅ `reporting.md`  
✅ `notifications.md`  
✅ `identity.md`  
✅ `digital-twin.md` ← ¡ACABAMOS DE CREARLO!  
✅ `index.md` ← ¡ACABAMOS DE CREARLO!
