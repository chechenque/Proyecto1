# Arquitectura de LogiTrack Desktop

## 1. Objetivo

LogiTrack Desktop utiliza una arquitectura basada en la separación de responsabilidades entre la interfaz gráfica, el ViewModel, el Controller, los servicios y los modelos de datos.

El objetivo principal es evitar que la interfaz contenga lógica de negocio o acceso directo a mecanismos de persistencia. De esta forma, cada componente puede evolucionar de manera independiente y el código resulta más fácil de probar y mantener.

La arquitectura utilizada combina principios de MVC y MVVM. El Controller coordina las operaciones de negocio y el acceso a los servicios, mientras que el ViewModel funciona como intermediario entre los datos y la interfaz gráfica.

## 2. Capas

### View

La capa View está representada principalmente por:

- `logitrack/views/main_window.py`

Sus responsabilidades son:

- Construir la interfaz gráfica.
- Configurar layouts y widgets.
- Recibir eventos del usuario.
- Mostrar mensajes y estados.
- Solicitar operaciones al ViewModel.

La View no debe contener reglas de negocio ni realizar directamente operaciones de persistencia.

### ViewModel

La capa ViewModel está representada por:

- `logitrack/controllers/shipment_view_model.py`

Sus responsabilidades son:

- Conectar la interfaz con el Controller.
- Solicitar operaciones sobre los envíos.
- Actualizar el modelo utilizado por la tabla.
- Exponer información preparada para la interfaz.
- Notificar cambios mediante señales de Qt.

Actualmente proporciona operaciones como:

- `create_shipment()`
- `search()`
- `refresh()`
- `count()`

### Controller

La capa Controller está representada por:

- `logitrack/controllers/shipment_controller.py`

Sus responsabilidades son:

- Recibir solicitudes del ViewModel.
- Validar datos de entrada.
- Coordinar las operaciones del dominio.
- Delegar las operaciones al Service.

Por ejemplo, antes de crear un envío verifica que el destinatario y la dirección sean obligatorios.

### Service

La capa Service está representada por:

- `logitrack/services/shipment_service.py`

Sus responsabilidades son:

- Ejecutar la lógica relacionada con los envíos.
- Crear y buscar registros.
- Mantener temporalmente los datos en memoria durante esta etapa del proyecto.
- Ejecutar operaciones que posteriormente podrán utilizar persistencia SQLite.

La lógica de negocio debe permanecer principalmente en esta capa y en el Controller cuando corresponda.

### Model

Los modelos representan los datos utilizados por la aplicación.

Actualmente se cuenta con:

- `logitrack/models/shipment_table_model.py`

`ShipmentTableModel` implementa `QAbstractTableModel` para proporcionar los datos a `QTableView`.

También se encarga de:

- Exponer filas y columnas.
- Proporcionar los valores mostrados.
- Gestionar la representación visual de los estados.
- Permitir ordenamiento de los registros.

## 3. Flujo de una operación

El flujo general para registrar un envío es:

```text
Usuario
   ↓
MainWindow (View)
   ↓
ShipmentViewModel
   ↓
ShipmentController
   ↓
ShipmentService
   ↓
Datos
```

Después de una operación exitosa, el flujo de actualización es:
```
ShipmentService
   ↓
ShipmentController
   ↓
ShipmentViewModel
   ↓
ShipmentTableModel
   ↓
QTableView
```

De esta manera, la interfaz no necesita conocer cómo se almacenan o procesan los datos.

## 4. Búsqueda de envíos

La búsqueda sigue el mismo principio:
```
Usuario
   ↓
MainWindow
   ↓
ShipmentViewModel.search()
   ↓
ShipmentController.search_shipments()
   ↓
ShipmentService.search_shipments()
   ↓
ShipmentTableModel
   ↓
QTableView
```

El ViewModel devuelve a la interfaz la cantidad de resultados encontrados, mientras que el modelo de tabla recibe los registros que deben mostrarse.

## 5. Operaciones asíncronas

Las operaciones potencialmente largas no deben ejecutarse directamente en el hilo principal de Qt.

LogiTrack utiliza:

* QThread
* QObject
* señales de Qt

El flujo es:
```
MainWindow
   ↓
QThread
   ↓
ShipmentWorker
   ↓
ShipmentService
```

El Worker ejecuta la operación fuera del hilo de interfaz y comunica el resultado mediante señales.

Esto permite que la ventana continúe respondiendo mientras se ejecuta una operación larga.

## 6. Principios de diseño

La arquitectura sigue los siguientes principios:

Separación de responsabilidades

Cada componente tiene una responsabilidad concreta y evita concentrar toda la lógica en la ventana principal.

Bajo acoplamiento

La View se comunica principalmente con el ViewModel y no necesita conocer los detalles internos del Service.

Reutilización

La lógica de negocio puede reutilizarse desde diferentes interfaces o pruebas sin depender directamente de los widgets de Qt.

Testabilidad

Los componentes de Controller y Service pueden probarse de forma independiente sin necesidad de iniciar toda la interfaz gráfica.

Responsividad

Las operaciones largas se ejecutan mediante mecanismos asíncronos para evitar bloquear el hilo principal.

Evolución

La arquitectura permite sustituir el almacenamiento temporal en memoria por SQLite sin modificar significativamente la interfaz gráfica.

## 7. Evolución hacia SQLite

En la siguiente etapa, el almacenamiento temporal utilizado por ShipmentService será reemplazado progresivamente por SQLite.

La arquitectura esperada será:

```
View
 ↓
ViewModel
 ↓
Controller
 ↓
Service
 ↓
Repository / SQLite
```

La interfaz continuará utilizando el mismo flujo de comunicación, mientras que la capa de persistencia será incorporada debajo del Service.

Esto permitirá que LogiTrack mantenga la separación entre interfaz, lógica de negocio y almacenamiento de datos.