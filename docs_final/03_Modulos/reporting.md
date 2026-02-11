¡Excelente! Vamos con el siguiente módulo clave: **Procurement** — el cerebro de compras, logística y gestión de proveedores de tu planta inteligente.

Este módulo no solo compra repuestos. **Optimiza inventarios, negocia con proveedores, sugiere reemplazos estratégicos, y hasta predice cuándo comprar antes de que se acabe algo crítico — todo con IA y datos en tiempo real.**

---

## 📄 `03-modulos/procurement.md` — LISTO PARA COPIAR Y PEGAR

```markdown
# 💰 Módulo: Procurement — Gestión Inteligente de Compras y Proveedores

> **Sistema autónomo de adquisiciones industriales: compra lo que se necesita, cuando se necesita, al mejor costo — con IA predictiva, integración de inventario, evaluación de proveedores y control de proyectos de capital.**

---

## 🎯 Propósito

El **Procurement Module** es el subsistema responsable de:

- **Gestionar compras de repuestos y materiales** (MRO: Maintenance, Repair, Operations).
- **Predecir necesidades de compra** antes de que el inventario llegue a cero.
- **Evaluar y seleccionar proveedores** por costo, calidad, tiempo de entrega y confiabilidad.
- **Gestionar órdenes de compra (POs)**, recepción, aprobación y pago.
- **Administrar proyectos de capital** (nuevas máquinas, upgrades, automatización).
- **Reducir costos totales de propiedad (TCO)** con análisis de ciclo de vida y alternativas.
- **Integrarse con inventario, mantenimiento y finanzas.**

> No es un sistema de compras tradicional. Es un **asistente predictivo de adquisiciones industriales** que evita paradas por falta de repuestos y optimiza cada dólar gastado.

---

## 🧩 Componentes Internos

```
[ Maintenance ] → (bajo stock) → [ Purchase Suggester ]
[ Assets ] → (vida útil)        → [ Capital Project Planner ]
                                   ↓
                          [ Supplier Evaluator ]
                                   ↓
                         [ Purchase Order Manager ]
                                   ↓
                        [ Receiving & Approval Flow ]
                                   ↓
                          [ Cost Analytics Engine ]
```

---

## 📥 Entradas Clave

- **Alertas de inventario bajo** (desde módulo Maintenance).
- **Predicciones de vida útil de activos** (desde Assets + IA).
- **Solicitudes manuales de compra** (ingenieros, técnicos, jefes).
- **Catálogo de proveedores** (precios, lead times, ratings).
- **Presupuestos por departamento/proyecto**.
- **Datos históricos de compras y rendimiento de proveedores**.

---

## 🧠 Purchase Suggester (Sugeridor Inteligente de Compras)

- **Función**: Genera sugerencias de compra automáticas.
- **Disparadores**:
  - Stock de repuesto < nivel mínimo (ajustado por IA).
  - Proyección de uso → stock se agotará en < 7 días.
  - Activo crítico → vida útil estimada < 6 meses → sugerir repuesto estratégico.
- **Salida**: Solicitud de compra sugerida con:
  - Artículo + cantidad.
  - Proveedores sugeridos (ordenados por score).
  - Costo estimado.
  - Urgencia (Baja, Media, Alta, Crítica).

> ✅ Las sugerencias se convierten en POs con un clic — o se aprueban automáticamente si son de bajo costo y proveedor confiable.

---

## 🏗️ Capital Project Planner (Planificador de Proyectos de Capital)

- **Función**: Gestiona compras de alto valor (nuevas máquinas, robots, líneas).
- **Flujo**:
  1. Ingeniero crea “Proyecto de Automatización Línea 4”.
  2. Sistema sugiere proveedores de robots, PLCs, sensores.
  3. Calcula ROI estimado (basado en reducción de scrap, aumento de OEE).
  4. Genera presupuesto → envía a aprobación gerencial.
  5. Si se aprueba → convierte en POs + cronograma de entrega.
- **Integración con módulo de proyectos** (futuro).

---

## ⭐ Supplier Evaluator (Evaluador de Proveedores)

- **Función**: Asigna un “score” a cada proveedor para cada tipo de artículo.
- **Criterios**:
  - Precio (peso 30%)
  - Tiempo de entrega promedio (peso 25%)
  - Calidad (devoluciones, reclamos) (peso 25%)
  - Confiabilidad (entregas a tiempo) (peso 20%)
- **Tabla `suppliers`**:
  ```sql
  CREATE TABLE suppliers (
      id SERIAL PRIMARY KEY,
      name VARCHAR(200) NOT NULL,
      contact TEXT,
      rating FLOAT DEFAULT 5.0, -- 1-5
      avg_delivery_days INTEGER,
      return_rate FLOAT,        -- % de devoluciones
      reliability_score FLOAT,  -- 0-100
      categories TEXT[],        -- ['rodamientos', 'motores', 'sensores']
      last_order_date TIMESTAMPTZ,
      metadata JSONB            -- contratos, condiciones, histórico
  );
  ```
- **IA de recomendación**: Sugiere proveedor óptimo por artículo + urgencia.

---

## 📄 Purchase Order Manager (Gestor de Órdenes de Compra)

- **Función**: Crea, envía, rastrea y archiva órdenes de compra.
- **Campos de una PO**:
  - ID único
  - Proveedor
  - Artículo(s) + cantidades + precios
  - Fecha estimada de entrega
  - Estado (Borrador, Enviada, Parcialmente Recibida, Completa, Cancelada)
  - Aprobadores requeridos (según monto)
  - Enlace a OT o proyecto (si aplica)
- **Notificaciones**:
  - Al proveedor (email/API).
  - Al solicitante (“PO enviada, entrega estimada: 5 días”).
  - Al almacén (“Preparar recepción de PO #204”).

---

## 📦 Receiving & Approval Flow (Flujo de Recepción y Aprobación)

- **Función**: Registra recepción de materiales y aprueba pagos.
- **Pasos**:
  1. Almacén escanea QR de paquete → sistema muestra PO asociada.
  2. Verifica cantidad y calidad → registra en sistema.
  3. Si hay discrepancia → genera alerta + notifica a compras.
  4. Si todo OK → marca PO como “Recibida” → notifica a finanzas para pago.
  5. Actualiza inventario automáticamente.
- **App móvil para almacén**: Escaneo QR, fotos de daños, firma digital.

---

## 📊 Cost Analytics Engine (Motor de Análisis de Costos)

- **Función**: Mide y optimiza gastos de adquisición.
- **KPIs**:
  - Costo total de mantenimiento por máquina/línea.
  - % de compras automatizadas vs manuales.
  - Ahorro generado por IA (vs compra manual).
  - TCO (Total Cost of Ownership) por activo.
- **Dashboards**:
  - “Top 10 repuestos más caros”.
  - “Proveedores con mejor ROI”.
  - “Tendencia de costos mensuales”.

---

## 🔐 Seguridad y Auditoría

- **RBAC estricto**:
  - Solicitante: crear solicitudes.
  - Comprador: convertir en PO, negociar con proveedores.
  - Aprobador: autorizar POs > $X.
  - Almacén: registrar recepción.
  - Finanzas: aprobar pagos.
- **Auditoría completa**:
  - Quién creó, aprobó, modificó, recibió cada PO.
  - Historial de precios por proveedor.
  - Fotos y notas de recepción.

---

## 📈 Métricas Clave

- `procurement_po_total_value_monthly`
- `procurement_avg_delivery_days`
- `procurement_supplier_rating_avg`
- `procurement_ia_suggestion_acceptance_rate`
- `procurement_cost_savings_vs_manual`

---

## 🧪 Ejemplo de Flujo: Repuesto por Agotarse → PO Aprobada

1. Sensor de inventario → stock de “Rodamiento 6205” = 2 (mínimo = 5).
2. Purchase Suggester → genera sugerencia: “Comprar 10 unidades. Proveedor sugerido: ABC Bearings (score 92/100)”.
3. Sistema → envía notificación al comprador: “Sugerencia de compra lista para aprobación”.
4. Comprador → revisa → aprueba con un clic (monto < $500 → no requiere aprobación superior).
5. PO #205 → generada y enviada a ABC Bearings → email + API.
6. Proveedor → confirma entrega en 3 días.
7. Almacén → recibe paquete → escanea QR → verifica → sistema actualiza inventario a 12.
8. Cost Analytics → registra ahorro: “IA eligió ABC vs. XYZ → ahorro de $87 (12%)”.

⏱️ **Tiempo total desde alerta de inventario hasta reposición: < 4 días.**

---

## 📁 Estructura de Código Recomendada

```
backend/
├── procurement/
│   ├── __init__.py
│   ├── purchase_suggester.py
│   ├── capital_project_planner.py
│   ├── supplier_evaluator.py
│   ├── po_manager.py
│   ├── receiving_flow.py
│   └── cost_analytics.py
├── models/
│   └── procurement_models.py  # Pydantic models
└── database/
    └── db_procurement.py      # Acceso a suppliers, purchase_orders

mobile_app/
└── src/
    └── screens/
        ├── PurchaseSuggestionList.js
        ├── POApproval.js
        └── ReceivingScanner.js
```

---

## 🧭 ¿Cómo empezar a desarrollar?

```bash
# 1. Ejecuta este script SQL en PostgreSQL

-- Tabla de proveedores
CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    contact TEXT,
    rating FLOAT DEFAULT 5.0,
    avg_delivery_days INTEGER,
    return_rate FLOAT,
    reliability_score FLOAT,
    categories TEXT[],
    last_order_date TIMESTAMPTZ,
    metadata JSONB
);

-- Tabla de órdenes de compra
CREATE TABLE purchase_orders (
    id SERIAL PRIMARY KEY,
    supplier_id INTEGER REFERENCES suppliers(id),
    status VARCHAR(20) DEFAULT 'draft', -- 'draft', 'sent', 'partial', 'completed', 'cancelled'
    total_value DECIMAL(12,2),
    requested_by INTEGER REFERENCES users(id),
    approved_by INTEGER REFERENCES users(id),
    expected_delivery_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    linked_maintenance_order_id INTEGER REFERENCES maintenance_orders(id),
    items JSONB  -- [{"part_code": "6205", "qty": 10, "unit_price": 15.50}]
);

-- Índices
CREATE INDEX idx_purchase_orders_status ON purchase_orders(status);
CREATE INDEX idx_purchase_orders_supplier ON purchase_orders(supplier_id);
CREATE INDEX idx_suppliers_rating ON suppliers(rating);

# 2. Levanta el módulo
uvicorn procurement.main:app --reload --port 8004

# 3. Crea tu primer proveedor
curl -X POST http://localhost:8004/suppliers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ABC Bearings",
    "contact": "ventas@abc.com",
    "rating": 4.8,
    "avg_delivery_days": 3,
    "categories": ["rodamientos", "sellos"]
  }'

# 4. Verifica en http://localhost:8004/suppliers
```

---

## 📌 Decisiones Clave

- **Sugerencias de compra automáticas** → evita paradas por falta de repuestos.
- **Score de proveedores dinámico** → mejora calidad y reduce costos.
- **POs con enlace a OTs/proyectos** → trazabilidad total.
- **App móvil para recepción** → reduce errores en almacén.
- **Análisis de costos en tiempo real** → toma de decisiones basada en datos.

---

> “Comprar bien no es gastar menos. Es gastar inteligente — en el momento justo, con el proveedor correcto, para el activo que más lo necesita.”

➡️ **Siguiente paso recomendado: definir el módulo de reporting (`reporting.md`) — dashboards ejecutivos, KPIs en tiempo real, reportes ESG, y visualización pública en la nube.**
```

---

## ✅ ACCIONES INMEDIATAS

1. Guarda este contenido como `procurement.md` en `03-modulos/`.
2. Ejecuta el script SQL en tu PostgreSQL.
3. Crea la carpeta `backend/procurement/` y los archivos `.py` vacíos.
4. ¡Celebra! Acabas de automatizar el flujo de dinero y materiales de tu fábrica.

---

## 🚀 PRÓXIMO DOCUMENTO: ¿QUÉ SIGUE?

> **Vamos con `reporting.md` — el cerebro de visualización: desde KPIs en tiempo real hasta reportes ESG para la web pública. Todo personalizable, exportable y seguro.**

¿Lo hacemos ahora? 👇  
O tomas un respiro — ¡lo estás haciendo increíble!

---

> Recuerda: **Una fábrica eficiente no solo produce bien. Compra bien, negocia bien, y gasta bien.  
> Este módulo asegura que cada dólar invertido en tu planta genere valor, no solo movimiento.**

¡Vamos por reporting! 📊🌐🧠

### USER
adelante

### ASSISTANT
¡VAMOS CON TODO! 🚀  
Ahora toca el módulo que **convierte datos en decisiones, números en estrategias, y tu fábrica en un modelo de transparencia y eficiencia** — el **Reporting Module**.

Este no es solo un dashboard bonito. Es tu **sala de guerra ejecutiva, tu ventana pública al mundo, y tu herramienta de mejora continua** — todo en uno.

---

## 📄 `03-modulos/reporting.md` — LISTO PARA COPIAR Y PEGAR

```markdown
# 📊 Módulo: Reporting — Visualización Inteligente y Reportes Ejecutivos

> **Sistema unificado de reportes, dashboards y KPIs en tiempo real — desde la pantalla del operario hasta el board de directores y la web pública. Personalizable, exportable, seguro y con IA embebida para insights automáticos.**

---

## 🎯 Propósito

El **Reporting Module** es el subsistema responsable de:

- **Visualizar KPIs industriales en tiempo real** (OEE, MTTR, MTBF, scrap rate, energía).
- **Generar dashboards personalizados por rol** (operario, supervisor, gerente, CEO).
- **Exportar reportes automáticos** (PDF, Excel, CSV) diarios/semanales/mensuales.
- **Publicar métricas anónimas en la web/cloud** (solo lectura, sin control).
- **Detectar automáticamente insights y anomalías** con IA (ej: “OEE cayó 15% en Línea 3”).
- **Integrarse con todos los módulos**: Core, IA, Mantenimiento, Activos, Procurement.

> No es “otro dashboard”. Es la **lente a través de la cual cada persona ve lo que necesita para actuar — en el momento preciso.**

---

## 🧩 Componentes Internos

```
[ Core Engine ] → (datos en vivo)    → [ Real-Time KPI Engine ]
[ Maintenance ] → (MTTR, MTBF)       → [ Performance Analytics ]
[ Assets ] → (salud, estado)         → [ Asset Health Dashboard ]
[ Procurement ] → (costos)           → [ Cost & Efficiency Reports ]
[ AI Orchestrator ] → (anomalías)    → [ Auto-Insights Generator ]
                                        ↓
                               [ Dashboard Builder ]
                                        ↓
                           [ Role-Based Views + Export ]
                                        ↓
                              [ Public Cloud Publisher ]
```

---

## 📥 Entradas Clave

- **Datos de sensores en tiempo real** (desde Core Engine).
- **Eventos de mantenimiento** (OTs, tiempos, repuestos).
- **Estado y salud de activos**.
- **Costos de adquisición y operación**.
- **Metas de producción y calidad**.
- **Predicciones y alertas de IA**.

---

## 📈 Real-Time KPI Engine (Motor de KPIs en Tiempo Real)

- **Función**: Calcula indicadores clave cada 10s-1min.
- **KPIs principales**:
  - **OEE (Overall Equipment Effectiveness)** = Disponibilidad × Rendimiento × Calidad
  - **MTTR (Mean Time To Repair)**
  - **MTBF (Mean Time Between Failures)**
  - **Scrap Rate (%)**
  - **Energy Consumption (kWh)**
  - **Production Rate (unidades/hora)**
- **Almacenamiento**: Tabla `kpi_snapshots` (TimescaleDB) → para histórico y tendencias.

> ✅ Cada KPI se calcula por máquina, línea, zona o planta completa.

---

## 🧠 Auto-Insights Generator (Generador Automático de Insights)

- **Función**: Detecta automáticamente cambios significativos y sugiere acciones.
- **Ejemplos**:
  - “⚠️ OEE de Línea 3 cayó 18% en las últimas 4 horas → posible causa: vibración anormal en Motor 7.”
  - “✅ Scrap rate bajó de 3.2% a 1.8% tras cambio de proveedor de materia prima (PO #205).”
  - “📈 MTBF de bombas aumentó 40% tras programa de lubricación predictiva.”
- **Tecnología**: Reglas simples + detección de anomalías estadísticas (Z-score, IQR).
- **Salida**: Notificaciones en dashboards + alertas push a roles relevantes.

---

## 🖥️ Dashboard Builder (Constructor de Dashboards)

- **Función**: Permite crear dashboards personalizados con arrastrar y soltar.
- **Widgets disponibles**:
  - Gráficos de tiempo (línea, barra, área).
  - Medidores (gauge) de salud/KPIs.
  - Tablas de eventos recientes.
  - Mapas de planta (SVG interactivo).
  - Indicadores de estado (semáforos).
  - Videos en vivo (cámaras IP, si integradas).
- **Guardado**: Cada usuario guarda sus layouts en `user_dashboards` (JSONB en PostgreSQL).

---

## 👥 Role-Based Views (Vistas por Rol)

| Rol               | Dashboard Principal                          | KPIs Clave                                  |
|-------------------|----------------------------------------------|---------------------------------------------|
| **Operario**      | Máquina asignada + OTs pendientes            | Estado, velocidad, temperatura, OTs         |
| **Supervisor**    | Línea completa + OTs abiertas                | OEE, scrap rate, MTTR, alertas              |
| **Ingeniero**     | Activos críticos + salud predictiva          | Vibración, temperatura, vida útil restante  |
| **Gerente Planta**| Toda la planta + comparativas                | OEE general, costos, energía, cumplimiento  |
| **CEO / Externo** | Solo KPIs agregados + tendencias             | Producción total, ESG, eficiencia energética|

> ✅ Cada rol ve SOLO lo que necesita — sin ruido, sin distracciones.

---

## 📤 Export Engine (Motor de Exportación)

- **Función**: Genera reportes programados o bajo demanda.
- **Formatos**: PDF, Excel, CSV, JSON.
- **Tipos de reportes**:
  - Diario de producción.
  - Semanal de mantenimiento.
  - Mensual de costos y eficiencia.
  - Anual de sostenibilidad (ESG).
- **Programación**: “Enviar reporte semanal de OEE a gerencia cada lunes 8am”.

---

## ☁️ Public Cloud Publisher (Publicador a Nube)

- **Función**: Expone **solo datos anónimos y agregados** en la web pública.
- **Qué se publica**:
  - Producción total del día (sin detalles de máquinas).
  - % de eficiencia energética.
  - Huella de carbono reducida.
  - Logros de sostenibilidad (ej: “Reciclamos 12 toneladas este mes”).
- **Tecnología**: API pública (FastAPI) + Frontend React ligero (solo lectura).
- **Seguridad**: Sin autenticación, sin endpoints de control, rate limiting.

> 🌍 Ideal para: sitio web corporativo, reportes ESG, inversionistas, clientes.

---

## 🔐 Seguridad y Auditoría

- **RBAC estricto**: Solo roles autorizados ven datos sensibles.
- **Máscara de datos**: En dashboards públicos, nunca se muestran valores reales de producción.
- **Auditoría de exports**: Quién exportó qué y cuándo.
- **Watermarking**: Reportes PDF llevan marca de usuario/fecha.

---

## 📈 Métricas Clave

- `reporting_active_dashboards_count`
- `reporting_auto_insights_generated`
- `reporting_exports_per_day`
- `reporting_public_api_requests`
- `reporting_user_satisfaction_score` (encuestas)

---

## 🧪 Ejemplo de Flujo: CEO Revisa Dashboard Matutino

1. CEO abre app web → login → dashboard ejecutivo.
2. Ve:
   - OEE general: 84% (▲ 3% vs semana pasada).
   - Producción: 12,500 unidades (meta: 12,000).
   - Energía: 8% más eficiente que meta.
   - Insight automático: “Línea 2 superó meta de calidad → replicar ajustes en Línea 4.”
3. Exporta reporte PDF → lo envía al board.
4. En la web pública → inversores ven: “Planta XYZ: 98% energía renovable, 15K ton CO2 evitadas.”

⏱️ **Tiempo total: < 5 minutos para tomar decisiones estratégicas.**

---

## 📁 Estructura de Código Recomendada

```
backend/
├── reporting/
│   ├── __init__.py
│   ├── kpi_engine.py
│   ├── auto_insights.py
│   ├── dashboard_builder.py
│   ├── export_engine.py
│   └── public_publisher.py
├── models/
│   └── reporting_models.py  # Pydantic models
└── database/
    └── db_reporting.py      # Acceso a kpi_snapshots, user_dashboards

web_app/
└── src/
    └── pages/
        ├── OperatorDashboard.js
        ├── SupervisorDashboard.js
        ├── ExecutiveDashboard.js
        └── PublicDashboard.js

mobile_app/
└── src/
    └── screens/
        ├── KpiSummary.js
        └── InsightDetail.js
```

---

## 🧭 ¿Cómo empezar a desarrollar?

```bash
# 1. Crea tabla de snapshots de KPIs (TimescaleDB)
CREATE TABLE kpi_snapshots (
    time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    machine_id INTEGER,
    line_id INTEGER,
    oee FLOAT,
    mttr FLOAT,
    mtbf FLOAT,
    scrap_rate FLOAT,
    energy_kwh FLOAT,
    production_rate FLOAT
);

SELECT create_hypertable('kpi_snapshots', 'time');

# 2. Crea tabla de dashboards de usuario
CREATE TABLE user_dashboards (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    layout JSONB NOT NULL,  -- estructura de widgets
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

# 3. Levanta el módulo
uvicorn reporting.main:app --reload --port 8005

# 4. Calcula primer KPI (simulado)
curl -X POST http://localhost:8005/reporting/calculate-kpi \
  -H "Content-Type: application/json" \
  -d '{"machine_id": 7, "oee": 87.4, "mttr": 2.1}'

# 5. Abre dashboard en http://localhost:3000 (si tienes frontend)
```

---

## 📌 Decisiones Clave

- **KPIs calculados en backend, no en frontend** → consistencia total.
- **Insights automáticos simples al inicio** → valor rápido sin IA compleja.
- **Dashboards personalizables** → cada usuario es único.
- **Exportación programada** → automatiza reportes rutinarios.
- **Nube solo para datos públicos/anónimos** → protege secretos industriales.

---

> “Un dato sin visualización es un secreto.  
> Una visualización sin contexto es ruido.  
> Un dashboard sin acción es arte.  
> Este módulo convierte datos en decisiones — y decisiones en resultados.”

➡️ **Siguiente paso recomendado: definir el módulo de notificaciones (`notifications.md`) — alertas en tiempo real, push, email, SMS, sirenas y tableros físicos.**
```

---

## ✅ ACCIONES INMEDIATAS

1. Guarda este contenido como `reporting.md` en `03-modulos/`.
2. Ejecuta el script SQL en tu PostgreSQL.
3. Crea la carpeta `backend/reporting/` y los archivos `.py` vacíos.
4. ¡Respira! Acabas de darle voz a los datos de tu fábrica — ahora todos, desde el operario hasta el CEO, pueden ver, entender y actuar.
