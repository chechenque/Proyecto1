LogiTrack Desktop — Widgets básicos

1. Objetivo

La segunda fase del proyecto implementa la primera versión funcional de la interfaz de LogiTrack Desktop.

El objetivo es proporcionar al despachador una pantalla desde la cual pueda registrar y consultar envíos rápidamente, sin depender de un navegador web.

En esta fase los datos se almacenan temporalmente en memoria. La persistencia mediante SQLite será implementada posteriormente en la Fase 7.

2. Componentes implementados

La ventana principal está compuesta por los siguientes elementos:

* QMainWindow: ventana principal de la aplicación.
* QLabel: títulos y textos informativos.
* QLineEdit: captura de destinatario y dirección.
* QComboBox: selección del tipo y estado del envío.
* QPushButton: acciones de guardar, limpiar y buscar.
* QTableWidget: visualización de los envíos.
* QGroupBox: agrupación visual del formulario.
* QFormLayout: organización de los campos del formulario.
* QHBoxLayout y QVBoxLayout: organización general de la interfaz.
* QStatusBar: comunicación del estado de las operaciones al usuario.

3. Funcionalidades

Alta de envíos

El usuario puede registrar un nuevo envío proporcionando:

* Destinatario.
* Dirección.
* Tipo de envío.
* Estado.

Al pulsar Guardar, el envío se agrega a la colección temporal y aparece en la tabla.

Limpieza del formulario

El botón Limpiar elimina los datos introducidos y devuelve los selectores a sus valores iniciales.

Búsqueda

El botón Buscar permite localizar envíos utilizando el nombre del destinatario o parte de la dirección.

Validación

El sistema verifica que los campos de destinatario y dirección no estén vacíos antes de registrar un envío.

Los errores se comunican mediante la barra de estado y el foco se devuelve al campo que requiere atención.

4. Manejo de eventos

Las acciones de los botones están conectadas mediante señales de PyQt6:
```
save_button.clicked.connect(self._save_shipment)
clear_button.clicked.connect(self._clear_form)
search_button.clicked.connect(self._search_shipments)
```
El flujo básico es:
```
Usuario
   │
   ▼
Pulsa botón
   │
   ▼
Señal clicked
   │
   ▼
Método correspondiente
   │
   ▼
Actualización de datos
   │
   ▼
Actualización de tabla / barra de estado
```
5. Estado actual

En esta fase los datos se mantienen en memoria mediante una lista de Python.

Esto es intencional. La persistencia permanente mediante SQLite se incorporará durante la Fase 7.

6. Evidencia

La siguiente captura demuestra el funcionamiento de la ventana, el formulario, la tabla y los controles principales:

7. Relación con L2

Esta fase demuestra los conocimientos correspondientes a la Lección 2:

* Creación de una ventana raíz.
* Uso de widgets básicos.
* Uso del bucle principal de Qt.
* Captura de información mediante formularios.
* Respuesta a eventos.
* Validación básica.
* Visualización de información mediante una tabla.
* Comunicación de estados al usuario.