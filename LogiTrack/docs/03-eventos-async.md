Fase 4 — Eventos, señales y tareas asíncronas

Objetivo

Implementar el manejo de eventos de la interfaz y ejecutar operaciones de larga duración en segundo plano para evitar el bloqueo del hilo principal de la aplicación.

Señales y eventos

LogiTrack Desktop utiliza el sistema de señales y slots de PyQt6 para responder a las acciones del usuario.

Algunos ejemplos son:

* El botón Guardar dispara el registro de un envío.
* El botón Limpiar reinicia el formulario.
* El botón Buscar ejecuta el filtrado de envíos.
* El botón Probar tarea asíncrona inicia una operación en segundo plano.

Los eventos de los botones se conectan mediante clicked.connect().

Problema del bloqueo de la interfaz

Las operaciones que requieren varios segundos no deben ejecutarse directamente en el hilo principal de Qt.

Una ejecución directa tendría la siguiente estructura:
```
Usuario
   │
   ▼
Botón
   │
   ▼
Operación de larga duración
   │
   ▼
Hilo principal bloqueado
   │
   ▼
Interfaz congelada
```
Esto produciría una mala experiencia de usuario y no cumpliría con el requisito de mantener la aplicación responsive.

Implementación con QThread

Para resolver este problema se implementó un ShipmentWorker basado en QObject y un QThread.

La arquitectura utilizada es:
```
┌──────────────────────┐
│    MainWindow        │
│  Hilo de interfaz    │
└──────────┬───────────┘
           │
           │ inicia
           ▼
┌──────────────────────┐
│      QThread         │
│  Hilo secundario     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   ShipmentWorker     │
│                      │
│ operación prolongada │
└──────────┬───────────┘
           │
           │ finished
           ▼
┌──────────────────────┐
│    MainWindow        │
│ actualiza interfaz   │
└──────────────────────┘
```
El ShipmentWorker se mueve al hilo secundario mediante:
```
worker.moveToThread(thread)
```
La operación comienza cuando el hilo emite su señal started.

Comunicación mediante señales

El worker dispone de dos señales:
```
finished = pyqtSignal(str)
error = pyqtSignal(str)
```
finished comunica una operación exitosa a la ventana, mientras que error permite informar posibles errores.

Al finalizar la operación, el hilo se detiene mediante:
```
thread.quit()
```
y los objetos utilizados son liberados mediante deleteLater().

Prueba realizada

Se implementó una operación de prueba que tarda aproximadamente cinco segundos.

Durante la ejecución se comprobó que:

* La ventana continúa respondiendo.
* La ventana puede moverse.
* La ventana puede redimensionarse.
* Los controles continúan disponibles.
* La aplicación no se congela.
* Al terminar la operación se muestra el resultado en la barra de estado.

Resultado

La prueba fue satisfactoria.

La aplicación puede ejecutar una operación prolongada sin bloquear el hilo principal de la interfaz.

Esta implementación establece la base para futuras operaciones como:

* consultas a SQLite;
* consumo de APIs externas;
* sincronización de información;
* enriquecimiento de datos de envíos;
* procesamiento de información.

Conclusión

LogiTrack Desktop utiliza eventos, señales y ejecución en segundo plano mediante QThread para mantener una interfaz responsive.

La solución evita ejecutar operaciones prolongadas directamente en el hilo de la interfaz y establece una estructura reutilizable para las operaciones asíncronas que se incorporarán en fases posteriores.