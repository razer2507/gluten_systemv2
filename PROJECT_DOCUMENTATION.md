# Documentación del Proyecto: `gluten_system_v2`

Este documento describe la arquitectura y el modelo de datos del sistema para facilitar el trabajo de desarrollo y mantenimiento por parte de inteligencias artificiales y desarrolladores humanos.

## 1. Visión General
El proyecto `gluten_system_v2` es un sistema de gestión modular diseñado bajo un enfoque de **Dominio (Domain-Driven Design - DDD)**. Su objetivo es gestionar las operaciones de ventas, productos, clientes, gastos y análisis de crédito de un negocio.

## 2. Estructura del Proyecto

```text
/
├── config/             # Configuración del sistema (ej. base de datos)
├── domains/            # Módulos de dominio (agrupados por funcionalidad)
│   ├── clientes/
│   ├── detalle_ventas/
│   ├── gastos/
│   ├── productos/
│   └── ventas/
├── shared/             # Lógica, utilidades y excepciones compartidas
├── tests/              # Pruebas unitarias e integración
└── main.py             # Punto de entrada de la aplicación
```

## 3. Modelo de Datos (Diagrama ER)

El sistema se basa en el siguiente modelo relacional:

### Entidades Principales
*   **`clientes`**: Información de los clientes del negocio.
*   **`productos`**: Catálogo de productos disponibles.
*   **`ventas`**: Registro principal de transacciones de venta.
*   **`detalle_ventas`**: Ítems individuales dentro de una venta.
*   **`gastos`**: Registro de egresos.
*   **`usuarios`**: Gestión de credenciales de acceso.
*   **`analisis_credito`**: Seguimiento de ventas a crédito.
*   **`estados` / `referencias`**: Tablas auxiliares para categorización.

### Relaciones Clave
*   `clientes` 1 --- N `ventas`
*   `clientes` 1 --- N `analisis_credito`
*   `ventas` 1 --- N `analisis_credito`
*   `ventas` 1 --- N `detalle_ventas`
*   `productos` 1 --- N `detalle_ventas`

## 4. Guías para el Agente AI

Al trabajar en este proyecto, sigue estas directrices:

1.  **Mantener la Modularidad**: Toda lógica nueva debe residir dentro del directorio `domains/` correspondiente. No mezcles lógica de `clientes` con `ventas`, a menos que sea a través de servicios o utilidades en `shared/`.
2.  **Seguir el Esquema**: Las operaciones de base de datos deben reflejar fielmente la estructura definida en el diagrama ER.
3.  **Configuración**: La configuración de conexión a la base de datos se encuentra en `config/database.py`.
4.  **Calidad**: Antes de finalizar cualquier tarea, verifica que se mantenga la integridad referencial y sigue las convenciones existentes.
5.  **Pruebas**: Toda funcionalidad nueva debe ir acompañada de un caso de prueba en `tests/`.
