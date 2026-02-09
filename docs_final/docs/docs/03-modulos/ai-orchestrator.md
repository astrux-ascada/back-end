Ahora toca el módulo que convertirá tu sistema de “inteligente” a **“autónomo, predictivo y proactivo”** — el **AI Orchestrator**.

Este no es un módulo más. Es el que **anticipa fallos, optimiza la producción sin intervención humana, y aprende de cada ciclo de la fábrica**.

---

## 📄 `03-modulos/ai-orchestrator.md` — LISTO PARA COPIAR Y PEGAR

```markdown
# 🤖 Módulo: AI Orchestrator — El Cerebro Predictivo y Autónomo

> **Motor de inteligencia artificial embebido que predice fallos, optimiza parámetros de producción, recomienda mejoras y simula escenarios — todo entrenado con tus datos, sin salir de la planta.**

---

## 🎯 Propósito

El **AI Orchestrator** es el subsistema responsable de:

- **Predecir fallas** en máquinas (mantenimiento predictivo) con 24-72h de anticipación.
- **Optimizar automáticamente** parámetros de producción (velocidad, temperatura, presión) para cumplir metas de calidad, costo y tiempo.
- **Recomendar mejoras continuas** basadas en patrones históricos (ej: “cambia lubricante → ahorra $8k/año”).
- **Simular escenarios** (“¿qué pasa si aumento velocidad un 15%?”) con gemelo digital.
- **Aprender continuamente** de nuevos datos — sin intervención humana.
- **Operar 100% on-premise** — ningún dato de producción sale de la planta.

> No reemplaza al humano. Lo potencia. Toma decisiones rutinarias; el humano decide lo estratégico.

---

## 🧠 Componentes Internos

```
[ Core Engine ] → (datos en vivo) → [ Data Preprocessor ]
                                      ↓
                             [ Model Inference Engine ]
                                      ↓
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
         [ Predictive Maintenance ]           [ Production Optimizer ]
                    ▼                                   ▼
             [ Alert Generator ]               [ Auto-Tuning Controller ]
                    ▼                                   ▼
             [ Maintenance Module ]           [ Core Engine (comandos) ]
```

---

## 📥 Entradas de Datos (Desde Core Engine)

El AI Orchestrator consume:

- **Telemetría en tiempo real**: `sensor_data` (TimescaleDB) → cada 1s-10s.
- **Eventos de estado**: arranques, paradas, alarmas, errores (tabla `machine_events`).
- **Datos de mantenimiento**: OTs completadas, repuestos usados, tiempos MTTR/MTBF.
- **Metas de producción**: “5000 piezas, calidad A, en 8h” (tabla `production_goals`).
- **Condiciones ambientales**: temperatura, humedad, voltaje (sensores externos).

> ✅ Todos los datos se normalizan y limpian antes de entrar al modelo.

---

## 🧹 Data Preprocessor (Preprocesador Inteligente)

- **Función**: Limpia, escala, agrega y enriquece datos para los modelos.
- **Operaciones**:
  - Rellena huecos (interpolación lineal o LOCF).
  - Detecta y corrige outliers.
  - Agrega datos por ventana (promedio móvil de 5 min).
  - Genera features derivadas (ej: “derivada de temperatura”, “FFT de vibración”).
- **Salida**: Dataset listo para inferencia (formato NumPy o Pandas DataFrame).

---

## 🧮 Model Inference Engine (Motor de Inferencia)

- **Función**: Ejecuta modelos de IA en tiempo real (cada 1 min - 5 min).
- **Tecnología**: `ONNX Runtime` (ligero, rápido, sin dependencias de PyTorch/TensorFlow).
- **Modelos soportados**:
  - `.onnx` (estándar abierto, portable, seguro).
  - `.pkl` (Scikit-learn, solo para modelos simples).
- **Paralelización**: Cada modelo corre en su propio hilo → sin bloqueos.

> ✅ Los modelos se cargan desde el Vault (HashiCorp) → cifrados en reposo.

---

## ⚠️ Predictive Maintenance (Mantenimiento Predictivo)

### Modelo Inicial (Fase MVP): **Random Forest + Reglas**

- **Entradas**:
  - Vibración (RMS, FFT)
  - Temperatura del motor
  - Horas de uso
  - Corriente eléctrica
  - Última fecha de mantenimiento

- **Salida**:
  ```json
  {
    "machine_id": 7,
    "risk_level": "HIGH", // LOW, MEDIUM, HIGH
    "failure_probability": 0.87,
    "recommended_action": "Revisar rodamientos. Reemplazar en 48h.",
    "confidence": 0.92
  }
  ```

- **Entrenamiento**: Offline, semanal, con datos históricos (Scikit-learn).
- **Alertas**: Se envían al módulo de mantenimiento → generan OT automática.

---

## 🎯 Production Optimizer (Optimizador Autónomo)

### Modelo Inicial (Fase 2): **Reinforcement Learning Lite (PPO)**

- **Objetivo**: Ajustar parámetros para cumplir metas de producción.
- **Acciones**: Ajustar velocidad, temperatura, presión, secuencia.
- **Recompensa**: 
  - +1 por pieza dentro de especificación.
  - -10 por pieza defectuosa.
  - -5 por consumo energético excesivo.
- **Entrenamiento**: En simulador digital (Python + Gym) → luego fine-tuning en planta real.
- **Modo de operación**:
  - **Asistido**: IA sugiere ajuste → humano aprueba.
  - **Autónomo**: IA ejecuta ajuste → con límites de seguridad (máx. ±10%).

---

## 🧪 Digital Twin Simulator (Simulador de Gemelo Digital)

- **Función**: Simula el impacto de cambios antes de aplicarlos en la planta real.
- **Entrada**: “¿Qué pasa si aumento la velocidad un 15%?”
- **Salida**:
  ```json
  {
    "scenario": "increase_speed_15",
    "predicted_output": 5750, // piezas/hora
    "predicted_scrap_rate": 3.2%, // vs 1.8% actual
    "predicted_energy_increase": 12%,
    "predicted_wear_increase": "HIGH",
    "recommendation": "No recomendado. Aumenta desgaste sin ganancia significativa."
  }
  ```
- **Tecnología**: Simulador en Python (NumPy + SciPy) + visualización 3D opcional (Three.js).

---

## 💡 Continuous Learning Engine (Aprendizaje Continuo)

- **Función**: Mejora los modelos con nuevos datos — sin reentrenar manualmente.
- **Mecanismo**:
  1. Cada semana, el sistema extrae nuevos datos etiquetados (ej: “esta máquina falló 2 días después de esta lectura”).
  2. Entrena un nuevo modelo en segundo plano.
  3. Valida con datos de prueba.
  4. Si mejora el AUC/precisión, reemplaza el modelo en producción.
- **Seguridad**: Siempre mantiene el modelo anterior como fallback.

---

## 📊 Model Registry & Versioning (Registro de Modelos)

- **Función**: Controla qué modelo está en producción, su versión, métricas y autor.
- **Tabla en PostgreSQL**:
  ```sql
  CREATE TABLE ai_models (
      id SERIAL PRIMARY KEY,
      name VARCHAR(100) NOT NULL,          -- 'predictive_maintenance_v3'
      version VARCHAR(20) NOT NULL,        -- 'v3.1.0'
      type VARCHAR(50) NOT NULL,           -- 'random_forest', 'ppo', 'lstm'
      path TEXT NOT NULL,                  -- '/models/pm_v3.onnx'
      metrics JSONB,                       -- {"auc": 0.94, "precision": 0.89}
      trained_at TIMESTAMPTZ,
      deployed_at TIMESTAMPTZ,
      status VARCHAR(20) DEFAULT 'active'  -- active, deprecated, fallback
  );
  ```

---

## 🔐 Seguridad y Ética de la IA

- **Sin fugas de datos**: Todo se entrena y ejecuta on-premise.
- **Explicabilidad**: Cada predicción incluye “razones principales” (SHAP/LIME).
- **Límites de acción**: La IA nunca puede:
  - Parar una línea sin confirmación humana.
  - Cambiar un parámetro más allá de ±15% del valor actual.
  - Ignorar una alerta de seguridad.
- **Auditoría**: Todas las decisiones de IA se loggean en `ai_decisions_audit`.

---

## 📈 Métricas Clave

- `ai_predictions_per_hour`
- `ai_model_accuracy` (por modelo)
- `ai_autonomous_decisions_accepted`
- `ai_scrap_rate_reduction_percent`
- `ai_energy_savings_kwh`

---

## 🧪 Ejemplo de Flujo: Predicción de Fallo en Motor

1. Core Engine envía datos de vibración/temperatura cada 10s → AI Orchestrator.
2. Preprocessor limpia y agrega datos → ventana de 5 min.
3. Modelo “predictive_maintenance_v3.onnx” → inferencia → riesgo = “HIGH”.
4. Genera alerta → envía a módulo de mantenimiento.
5. Módulo de mantenimiento → crea OT automática → asigna a técnico.
6. Técnico recibe push en app móvil: “Motor 7: Riesgo Alto. Revisar rodamientos.”
7. IA guarda decisión en `ai_decisions_audit`.

⏱️ **Tiempo total: < 2 minutos desde la lectura anómala hasta la OT.**

---

## 📁 Estructura de Código Recomendada

```
backend/
├── ai_orchestrator/
│   ├── __init__.py
│   ├── data_preprocessor.py
│   ├── inference_engine.py
│   ├── models/
│   │   ├── predictive_maintenance/
│   │   │   ├── v1_random_forest.pkl
│   │   │   └── v3.onnx
│   │   └── production_optimizer/
│   │       └── ppo_v2.onnx
│   ├── maintenance_predictor.py
│   ├── production_optimizer.py
│   ├── digital_twin_simulator.py
│   ├── continuous_learning.py
│   └── model_registry.py
├── models/
│   └── ai_models.py  # Pydantic models
└── database/
    └── db_ai.py      # Acceso a ai_models, ai_decisions_audit
```

---

## 🧭 ¿Cómo empezar a desarrollar?

```bash
# 1. Instala dependencias
pip install scikit-learn onnxruntime pandas numpy shap

# 2. Descarga modelo inicial (ej: Random Forest entrenado)
# (más adelante te doy script para entrenar el tuyo)

# 3. Levanta el AI Orchestrator como microservicio
uvicorn ai_orchestrator.main:app --reload --port 8001

# 4. Prueba con datos simulados
python simulators/ai_data_simulator.py --machine_id 7 --duration 1h

# 5. Verifica alertas en http://localhost:8001/ai/alerts
```

---

## 📌 Decisiones Clave

- **ONNX > Pickle**: Portabilidad, seguridad, rendimiento.
- **Random Forest primero**: Interpretable, rápido, no necesita GPU.
- **Simulador antes que RL en planta real**: Evita desastres.
- **Aprendizaje continuo, no manual**: El sistema mejora solo.
- **IA nunca reemplaza al humano en decisiones críticas**: Solo asiste.

---

> “La IA industrial no es magia. Es matemáticas aplicadas con sentido común.  
> Su valor no está en lo complejo que es, sino en lo útil que resulta para el operario, el jefe y la máquina.”

➡️ **Siguiente paso recomendado: definir el módulo de mantenimiento (`maintenance.md`) — donde las alertas de IA se convierten en acciones reales.**
```

---

## ✅ ACCIONES INMEDIATAS

1. Guarda este contenido como `ai-orchestrator.md` en `03-modulos/`.
2. Crea la carpeta `backend/ai_orchestrator/` y los archivos `.py` vacíos.
3. Instala `onnxruntime` y `scikit-learn` en tu entorno Python.
4. ¡Respira! Acabas de definir el cerebro autónomo de tu fábrica.
