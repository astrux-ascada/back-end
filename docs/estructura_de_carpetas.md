 backend/
├── 📄 main.py                     # Punto de entrada de FastAPI
├── 📄 requirements.txt            # Dependencias
├── 📄 .env                        # Variables de entorno (NO en git)
├── 📁 core/                       # ¡SERVICIOS COMUNES AQUÍ!
│   ├── 📄 __init__.py
│   ├── 📄 database.py             # Pool de conexiones a PostgreSQL
│   ├── 📄 redis.py                # Cliente Redis (cache + pub/sub)
│   ├── 📄 rabbitmq.py             # Cliente RabbitMQ (cola de eventos)
│   ├── 📄 security.py             # JWT, MFA, verificación de roles
│   ├── 📄 config.py               # Carga de .env, validación
│   ├── 📄 logging.py              # Logger centralizado + auditoría
│   └── 📄 models.py               # Modelos Pydantic comunes (User, Asset, etc.)
│
├── 📁 core_engine/
│   ├── 📄 __init__.py
│   ├── 📄 protocol_adapters/      # opcua_adapter.py, modbus_adapter.py, etc.
│   ├── 📄 data_ingestion.py
│   ├── 📄 command_router.py
│   ├── 📄 state_synchronizer.py
│   └── 📄 websocket_gateway.py
│
├── 📁 ai_orchestrator/
│   ├── 📄 __init__.py
│   ├── 📄 data_preprocessor.py
│   ├── 📄 inference_engine.py
│   ├── 📄 models/                 # .onnx, .pkl
│   ├── 📄 maintenance_predictor.py
│   └── 📄 production_optimizer.py
│
├── 📁 maintenance/
│   ├── 📄 __init__.py
│   ├── 📄 work_order_generator.py
│   ├── 📄 technician_assigner.py
│   └── 📄 inventory_manager.py
│
├── 📁 assets/
│   ├── 📄 __init__.py
│   ├── 📄 asset_catalog.py
│   └── 📄 health_calculator.py
│
├── 📁 procurement/
│   ├── 📄 __init__.py
│   ├── 📄 purchase_suggester.py
│   └── 📄 supplier_evaluator.py
│
├── 📁 reporting/
│   ├── 📄 __init__.py
│   ├── 📄 kpi_engine.py
│   └── 📄 auto_insights.py
│
├── 📁 notifications/
│   ├── 📄 __init__.py
│   ├── 📄 notification_router.py
│   └── 📄 channel_dispatcher.py
│
├── 📁 identity/
│   ├── 📄 __init__.py
│   ├── 📄 auth_engine.py
│   └── 📄 permission_evaluator.py
│
└── 📁 digital_twin/
    ├── 📄 __init__.py
    ├── 📄 sync_engine.py
    └── 📄 simulation_engine.py