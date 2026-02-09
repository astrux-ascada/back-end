 🌴 Caso de Uso: Planta de Aceite de Palma — Automatización con Orquestador Industrial 5.0

> **Cómo el sistema transforma una planta real: desde molinos hasta envasado, con IA predictiva, mantenimiento autónomo y control total.**

---

## 🏭 Descripción de la Planta

- **Proceso**: Recepción → Esterilización → Prensado → Clarificación → Envasado.
- **Máquinas Críticas**: 
  - Molinos de fruta.
  - Prensas hidráulicas.
  - Centrífugas de clarificación.
  - Tanques de almacenamiento.
  - Línea de envasado automática.
- **Dolor Actual**:
  - Paradas no planeadas por fallas mecánicas.
  - Scrap alto por variación de temperatura en prensado.
  - Mantenimiento reactivo → costos altos.
  - Sin visión unificada → datos en 5 pantallas distintas.

---

## 🎯 Objetivos con Orquestador Industrial 5.0

1. Reducir paradas no planeadas en 40% en 6 meses.
2. Optimizar temperatura de prensado → reducir scrap en 25%.
3. Implementar mantenimiento predictivo en molinos y centrífugas.
4. Controlar toda la planta desde tablets en piso.
5. Mostrar KPIs públicos en web: sostenibilidad, eficiencia energética.

---

## 🔄 Flujos Clave Implementados

### 1. Predicción de Falla en Molino

- **Sensor**: Vibración + temperatura del eje.
- **IA**: Random Forest → alerta 48h antes.
- **Acción**: OT automática → técnico reemplaza rodamiento → evita parada de 8h.

### 2. Optimización Autónoma de Prensado

- **Meta**: “Máxima extracción, mínimo scrap”.
- **IA**: Reinforcement Learning → ajusta temperatura y presión en tiempo real.
- **Resultado**: Scrap reducido de 8% a 5.5%.

### 3. Control Remoto de Centrífugas

- **Operario**: Desde tablet → “Aumentar velocidad 5%” → MFA → confirmación → comando ejecutado.
- **Seguridad**: Solo en turno, solo para supervisores.

### 4. Dashboard Público

- **Web**: “Planta XYZ: 98% energía renovable, 15K ton CO2 evitadas este año.”
- **API Pública**: KPIs diarios para socios e inversionistas.

---

## 📈 Resultados Esperados (12 Meses)

| KPI               | Antes | Después | Reducción/Aumento |
|-------------------|-------|---------|-------------------|
| Paradas no planeadas | 12/mes | 5/mes  | -58%              |
| Scrap rate        | 8%    | 5.5%    | -31%              |
| MTTR              | 4.2h  | 1.8h    | -57%              |
| Costo mantenimiento | $25K/mes | $16K/mes | -36%          |
| Satisfacción operarios | 3.2/5 | 4.7/5 | +47%          |

---

## 🧭 Próximos Pasos

1. Instalar sensores en molinos y prensas.
2. Conectar PLCs de centrífugas y envasado.
3. Entrenar primer modelo con datos históricos.
4. Capacitar a 20 operarios en app móvil.

> “Una planta de aceite de palma no es solo máquinas. Es un ecosistema. Y este sistema es su nuevo sistema nervioso.”
```
