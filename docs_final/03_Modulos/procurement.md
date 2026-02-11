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
