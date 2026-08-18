# LogiTrack Desktop — Fundamentos y elección de framework

## 1. Contexto

LogiTrack Desktop es una aplicación de escritorio para operadores de
sucursales de una empresa ficticia de logística y paquetería.

El sistema permitirá registrar, consultar, filtrar y actualizar envíos
desde una computadora de mostrador, incluso en escenarios donde la
conectividad a Internet sea inestable.

La aplicación debe proporcionar una interfaz rápida, estable y fácil de
utilizar, sin depender de un navegador web.

---

## 2. Comparativa de frameworks GUI

| Criterio | Tkinter | PyQt6 | Kivy | Flet |
|---|---|---|---|---|
| Facilidad inicial | Alta | Media | Media | Alta |
| Widgets avanzados | Medio | Excelente | Bueno | Bueno |
| Tablas y vistas complejas | Medio | Excelente | Medio | Bueno |
| Señales/eventos | Bueno | Excelente | Bueno | Bueno |
| Personalización visual | Medio | Excelente | Excelente | Bueno |
| Arquitectura GUI | Bueno | Excelente | Bueno | Bueno |
| Aplicaciones de escritorio | Excelente | Excelente | Bueno | Bueno |
| Look & Feel de escritorio | Bueno | Excelente | Medio | Bueno |
| Comunidad/ecosistema | Muy grande | Muy grande | Grande | En crecimiento |
| Empaquetado | Bueno | Bueno | Bueno | Bueno |
| Adecuación para LogiTrack | 🟡 | 🟢 | 🟡 | 🟡 |

---

## 3. Framework seleccionado

### PyQt6

El framework seleccionado para LogiTrack Desktop es PyQt6.

### Justificación

LogiTrack Desktop requiere una interfaz de escritorio que pueda crecer
desde una ventana sencilla hasta una aplicación con múltiples componentes
visuales, tablas, formularios, filtros, indicadores de estado y diferentes
vistas. PyQt6 resulta adecuado porque proporciona un conjunto amplio de
widgets y herramientas diseñadas específicamente para aplicaciones de
escritorio.

Uno de los principales motivos de la elección es el sistema de señales y
slots de Qt. Este mecanismo permite separar los eventos producidos por la
interfaz de la lógica que debe ejecutarse como consecuencia de ellos. Esto
será especialmente importante en LogiTrack cuando implementemos consultas
a SQLite y llamadas a servicios externos sin bloquear la interfaz.

Otro factor importante es la arquitectura. Qt facilita la separación entre
las vistas, los controladores y los servicios de la aplicación, lo que
permite implementar el patrón MVC definido para LogiTrack.

Finalmente, PyQt6 puede empaquetarse mediante PyInstaller, permitiendo
generar un ejecutable distribuible para usuarios que no tengan Python
instalado.

---

## 4. Evidencia de la elección

La primera prueba de concepto consiste en una ventana mínima ejecutable
mediante:

```bash
python -m logitrack
```

La aplicación muestra una ventana cuyo título es:

LogiTrack Desktop

Esta prueba demuestra que el framework seleccionado se encuentra
correctamente instalado y que el proyecto puede ejecutarse mediante un
módulo Python.

## 5. Estructura inicial
```
LogiTrack/
├── docs/
│   └── 00-fundamentos.md
├── logitrack/
│   ├── __init__.py
│   ├── __main__.py
│   └── app.py
├── tests/
├── scripts/
├── requirements.txt
└── README.md
```