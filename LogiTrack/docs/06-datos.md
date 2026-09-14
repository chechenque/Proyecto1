06 — Datos, persistencia y API

Objetivo

LogiTrack Desktop utiliza una arquitectura de persistencia local basada en SQLite y modelos de datos validados mediante Pydantic. Esta combinación permite que la aplicación funcione sin depender permanentemente de un servidor externo y proporciona una base sólida para trabajar en escenarios donde la conexión a Internet puede ser inestable.

Además de la persistencia local, la aplicación integra un servicio HTTP externo para consultar información asociada a códigos postales de México. Las consultas se ejecutan mediante operaciones asíncronas para evitar que la interfaz gráfica se bloquee mientras espera una respuesta de red.

La arquitectura separa el acceso a los datos de la interfaz mediante las capas Repository, Service, Controller y ViewModel.

⸻

1. Persistencia con SQLite

La aplicación utiliza SQLite como base de datos local.

La conexión se administra mediante la clase:

logitrack/models/database.py

La clase Database se encarga de:

* Crear el directorio de la base de datos cuando es necesario.
* Abrir conexiones SQLite.
* Configurar sqlite3.Row para acceder a las columnas mediante nombre.
* Inicializar las tablas requeridas por la aplicación.

La base de datos no requiere un servidor externo, por lo que resulta adecuada para una aplicación de escritorio y para escenarios con conectividad limitada.

Tabla shipments

La información de los envíos se almacena en la tabla:

```sqlite
CREATE TABLE IF NOT EXISTS shipments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient TEXT NOT NULL,
    address TEXT NOT NULL,
    shipment_type TEXT NOT NULL,
    status TEXT NOT NULL
)
```
Los principales datos almacenados son:

| Campo         | Tipo    | Descripción                  |
|---------------|---------|------------------------------|
| id            | INTEGER | Identificador único          |
| recipient     | TEXT    | Nombre del destinatario      |
| address       | TEXT    | Dirección de entrega         |
| shipment_type | TEXT    | Tipo de envío                |
| status        | TEXT    | Estado actual del envío      |

⸻

2. Modelo de datos con Pydantic

Los datos de los envíos se representan mediante el modelo:

logitrack/models/shipment.py

El modelo utiliza Pydantic v2 para realizar validaciones antes de almacenar información.

Entre las validaciones implementadas se encuentran:

* El destinatario es obligatorio.
* La dirección es obligatoria.
* El destinatario tiene una longitud máxima.
* La dirección tiene una longitud máxima.
* El tipo de envío debe contener información.
* El estado debe contener información.

Esto evita que datos inválidos lleguen directamente a la capa de persistencia.

El uso de Pydantic también permite mantener una representación estructurada de los datos y facilita las pruebas unitarias.

⸻

3. Repository

El acceso directo a SQLite se concentra en los repositorios.

Para los envíos se utiliza:
```
logitrack/models/shipment_repository.py
```
El repositorio se encarga de operaciones como:

* Crear envíos.
* Obtener todos los envíos.
* Buscar envíos.
* Convertir los registros de SQLite en estructuras utilizables por la aplicación.

La interfaz gráfica no realiza consultas SQL directamente.

El flujo utilizado es:
```
View
  ↓
ViewModel
  ↓
Controller
  ↓
Service
  ↓
Repository
  ↓
SQLite
```
Esta separación facilita las pruebas y permite cambiar posteriormente la implementación de persistencia sin modificar la interfaz.

⸻

4. API externa de códigos postales

LogiTrack también utiliza un servicio HTTP externo para consultar información de códigos postales.

El cliente se encuentra en:
```
logitrack/services/address_api_client.py
```
El cliente utiliza httpx para realizar las solicitudes.

El servicio utilizado es:

https://api.zippopotam.us/MX

Una consulta se realiza utilizando el código postal proporcionado por el usuario.

La respuesta se transforma en una estructura sencilla:
```json
{
    "city": "...",
    "state": "..."
}
```
De esta manera, la interfaz solamente necesita trabajar con la información relevante y no con toda la respuesta original de la API.

⸻

5. Validación del código postal

Antes de realizar la solicitud HTTP se valida el código postal.

El código postal debe:

* Contener únicamente dígitos.
* Tener exactamente cinco caracteres.

Si la validación falla, no se realiza ninguna solicitud externa.

Esto permite detectar errores de entrada antes de utilizar recursos de red.

⸻

6. Operaciones asíncronas

Las solicitudes a la API no se ejecutan directamente en el hilo principal de Qt.

Para la consulta de códigos postales se utiliza:

PostalCodeWorker

junto con:

QThread

El flujo es:
```
Usuario
   ↓
MainWindow
   ↓
ViewModel
   ↓
PostalCodeWorker
   ↓
QThread
   ↓
AddressApiClient
   ↓
API externa
```
Cuando la operación termina, el worker emite una señal finished o error.

Esto permite que la ventana continúe respondiendo mientras se realiza la consulta de red.

⸻

7. Manejo de conexión offline

Una de las características importantes de LogiTrack es su capacidad para trabajar ante una pérdida temporal de conexión.

Cuando una consulta de código postal no puede establecer conexión con el servicio externo, la aplicación registra la operación en una cola local.

Las operaciones se almacenan en:

offline_operations

La tabla contiene:
```sqlite
CREATE TABLE IF NOT EXISTS offline_operations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation TEXT NOT NULL,
    payload TEXT NOT NULL,
    status TEXT NOT NULL
)
```
Una operación pendiente utiliza el estado:

PENDING

Por ejemplo:
```
operation = postal_code_lookup
payload   = 01000
status    = PENDING
```
⸻

8. Sincronización de operaciones pendientes

Cuando el usuario recupera la conexión puede utilizar el botón:

Sincronizar

La sincronización se ejecuta mediante:

OfflineSyncWorker

El worker ejecuta la sincronización fuera del hilo de la interfaz.

El flujo es:
```
Usuario
   ↓
Sincronizar
   ↓
QThread
   ↓
OfflineSyncWorker
   ↓
ShipmentService
   ↓
Operaciones PENDING
   ↓
API de códigos postales
   ↓
SYNCED
```
Cuando una operación se procesa correctamente, su estado cambia de:

PENDING

a:

SYNCED

La interfaz actualiza entonces el contador de operaciones pendientes.

Por ejemplo:

Pendientes offline: 1

después de una sincronización exitosa pasa a:

Pendientes offline: 0

⸻

9. Separación de responsabilidades

El manejo de datos se distribuye entre diferentes capas.

Model

Representa y valida los datos.

Shipment
OfflineOperation

Repository

Realiza las operaciones de persistencia.

ShipmentRepository
OfflineOperationRepository

Service

Contiene la lógica relacionada con los datos y servicios externos.

ShipmentService
OfflineOperationService
AddressApiClient

Controller

Expone operaciones que puede utilizar la capa de presentación.

ShipmentController
OfflineOperationController

ViewModel

Conecta los datos y operaciones con la interfaz.

ShipmentViewModel
OfflineOperationViewModel

Esta separación evita colocar consultas SQL, solicitudes HTTP o lógica de negocio directamente dentro de los widgets de PyQt6.

⸻

10. Pruebas

La funcionalidad de datos y sincronización se valida mediante pruebas automatizadas.

Entre las pruebas implementadas se encuentran:

* Creación de envíos.
* Búsqueda de envíos.
* Validación de datos.
* Consulta de códigos postales.
* Manejo de errores de conexión.
* Registro de operaciones offline.
* Emisión de señales de operaciones offline.
* Sincronización de operaciones pendientes.
* Funcionamiento del OfflineSyncWorker.

También se utilizan bases de datos temporales durante las pruebas para evitar modificar la base de datos utilizada por la aplicación.

⸻

11. Resultado

La implementación permite que LogiTrack Desktop combine:

* Persistencia local.
* Validación estructurada.
* Consultas HTTP.
* Ejecución asíncrona.
* Manejo de pérdida de conexión.
* Cola offline.
* Sincronización posterior.
* Pruebas automatizadas.

Esto proporciona una base adecuada para una aplicación de escritorio que debe continuar siendo útil incluso cuando la conectividad de red no es constante.