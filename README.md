LogiTrack Desktop

Aplicación de escritorio para la gestión de envíos y operaciones logísticas.

Descripción

LogiTrack Desktop es una aplicación nativa desarrollada en Python y PyQt6 para gestionar envíos de una empresa ficticia de logística.

El proyecto está diseñado para operar en equipos de escritorio y contempla escenarios con conectividad inestable mediante persistencia local, operaciones asíncronas y una cola de operaciones offline.

La aplicación integra una arquitectura por capas que separa la interfaz gráfica, la lógica de presentación, el control de operaciones, los servicios y la persistencia de datos.

Objetivos

El proyecto busca demostrar el desarrollo de una aplicación de escritorio profesional que:

* Permita registrar y consultar envíos.
* Mantenga la interfaz responsiva durante operaciones prolongadas.
* Utilice persistencia local mediante SQLite.
* Valide los datos mediante Pydantic.
* Integre servicios HTTP externos.
* Permita trabajar con conectividad limitada.
* Sincronice operaciones pendientes cuando se restablece la conexión.
* Mantenga una separación clara de responsabilidades.
* Incluya pruebas automatizadas e integración continua.
* Pueda distribuirse como aplicación ejecutable.

Características

* Registro de envíos.
* Consulta y búsqueda de envíos.
* Persistencia local con SQLite.
* Validación de datos con Pydantic.
* Consulta de códigos postales mediante API HTTP.
* Procesamiento asíncrono mediante QThread.
* Cola de operaciones offline.
* Sincronización de operaciones pendientes.
* Tabla basada en QTableView.
* Ordenamiento de columnas.
* Indicadores visuales según el estado del envío.
* Tema claro y oscuro.
* Cambio de tema desde la interfaz.
* Atajos de teclado.
* Interfaz adaptable mediante layouts y QSplitter.
* Pruebas unitarias y de integración.
* Cobertura superior al 85%.
* Integración continua mediante GitHub Actions.
* Empaquetado mediante PyInstaller.

Tecnologías
```
Tecnología	Uso
Python 3.12	Lenguaje principal
PyQt6	Interfaz gráfica
Pydantic	Validación y modelos de datos
SQLite	Persistencia local
httpx	Cliente HTTP
pytest	Pruebas automatizadas
pytest-cov	Medición de cobertura
PyInstaller	Empaquetado
GitHub Actions	Integración continua
Git	Control de versiones
```
Arquitectura

LogiTrack Desktop utiliza una arquitectura por capas basada en la separación de responsabilidades:
```
┌──────────────────────────────┐
│            View              │
│        PyQt6 / UI            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         ViewModel            │
│   Estado y presentación      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         Controller           │
│    Control de operaciones    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           Service            │
│      Lógica de aplicación    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         Repository           │
│      Persistencia SQLite     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           SQLite             │
│       Base de datos local    │
└──────────────────────────────┘
```
Responsabilidades

View

Contiene los componentes visuales de PyQt6, layouts, botones, formularios, tablas y elementos relacionados con la presentación.

ViewModel

Coordina los datos que necesita la interfaz y comunica las acciones de la vista con el controlador.

Controller

Recibe las acciones de la interfaz y coordina las operaciones mediante los servicios correspondientes.

Service

Contiene la lógica de aplicación, integración HTTP, operaciones asíncronas y procesamiento relacionado con el funcionamiento offline.

Repository

Gestiona el acceso a SQLite y las operaciones de persistencia.

Estructura del proyecto
```
Proyecto1/
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── LogiTrack/
│   ├── docs/
│   │   ├── 00-fundamentos.md
│   │   ├── 01-widgets.md
│   │   ├── 02-layouts.md
│   │   ├── 03-eventos-async.md
│   │   ├── 04-componentes.md
│   │   ├── 05-arquitectura.md
│   │   ├── 06-datos.md
│   │   ├── 07-empaquetado.md
│   │   ├── 08-self-review.md
│   │   └── images/
│   │
│   ├── logitrack/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── services/
│   │   ├── ui/
│   │   ├── views/
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   └── app.py
│   │
│   ├── scripts/
│   │   ├── setup.sh
│   │   ├── setup.bat
│   │   └── build.spec
│   │
│   ├── tests/
│   │   ├── integration/
│   │   └── unit/
│   │
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── README.md
│
└── README.md
```
Instalación

Requisitos

* Python 3.11 o superior.
* Git.
* Sistema operativo compatible con Python y PyQt6.

Clonar el repositorio
```
git clone https://github.com/chechenque/Proyecto1.git
cd Proyecto1/LogiTrack
```
Crear el entorno virtual

En macOS con Homebrew:
```
/opt/homebrew/bin/python3.12 -m venv .venv
```
Activar el entorno:
```
source .venv/bin/activate
```
Instalar dependencias

Actualizar pip:
```
python -m pip install --upgrade pip
```
Instalar dependencias principales:
```
pip install -r requirements.txt
```
Para desarrollo y pruebas:
```
pip install -r requirements-dev.txt
```
Ejecución

Con el entorno virtual activo:
```
python -m logitrack
```
La aplicación abrirá la ventana principal de LogiTrack Desktop.

Funcionalidades principales

Registro de envíos

La aplicación permite registrar:

* Destinatario.
* Dirección.
* Código postal.
* Tipo de envío.
* Estado.

Los datos son validados antes de almacenarse.

Consulta de códigos postales

El sistema puede consultar información de ubicación mediante un servicio HTTP externo.

La consulta se ejecuta en un hilo de trabajo para evitar bloquear la interfaz gráfica.

Persistencia local

Los envíos y las operaciones offline se almacenan en una base de datos SQLite local.

La aplicación inicializa automáticamente las tablas necesarias.

Funcionamiento offline

Cuando una consulta de código postal no puede realizarse debido a una pérdida de conexión, la operación puede almacenarse como pendiente.

Las operaciones pendientes se muestran en la interfaz:

Pendientes offline: 1

Cuando existe conectividad nuevamente, las operaciones pueden sincronizarse mediante el botón:

Sincronizar

Procesamiento asíncrono

Las operaciones que pueden tardar varios segundos se ejecutan fuera del hilo principal mediante QThread y workers.

Esto permite que la interfaz continúe respondiendo mientras se ejecuta la operación.

Atajos de teclado
```
Atajo	Acción
Ctrl + G	Guardar envío
Ctrl + L	Limpiar formulario
Ctrl + B	Buscar envíos
Ctrl + M	Cambiar tema
```
Temas

La aplicación incluye:

* Tema claro.
* Tema oscuro.
* Cambio dinámico desde la interfaz.
* Cambio mediante Ctrl + M.

Los estilos se centralizan en:

logitrack/ui/theme.py

Esto evita distribuir valores de estilo arbitrarios por las diferentes vistas.

Pruebas

Las pruebas se ejecutan mediante pytest.

Desde la carpeta LogiTrack:

python -m pytest

La suite incluye pruebas para:

* Modelos.
* Repositorios.
* Servicios.
* Controladores.
* ViewModels.
* Workers.
* Operaciones offline.
* Integración de la interfaz principal.

Cobertura

La última medición registrada del proyecto alcanzó:

91%

Para generar nuevamente el reporte:
```
python -m pytest --cov=logitrack --cov-report=term-missing
```
Integración continua

El proyecto utiliza GitHub Actions para ejecutar automáticamente las pruebas.

El workflow se encuentra en:
```
.github/workflows/ci.yml
```
Actualmente verifica:

1. Checkout del repositorio.
2. Instalación de dependencias gráficas necesarias para PyQt6.
3. Configuración de Python 3.12.
4. Instalación de dependencias.
5. Ejecución de la suite de pruebas.

Debido a que los runners de GitHub Actions no cuentan con una interfaz gráfica tradicional, Qt se ejecuta mediante:

QT_QPA_PLATFORM: offscreen

La última ejecución validada de CI fue exitosa con:

80 tests

Empaquetado

El proyecto utiliza PyInstaller para generar un ejecutable.

El archivo de configuración se encuentra en:
```
scripts/build.spec
```
Para generar el ejecutable:
```
python -m PyInstaller --clean scripts/build.spec
```
El resultado se genera en:
```
dist/LogiTrack
```
Para ejecutar el binario generado en macOS:
```
./dist/LogiTrack
```
El empaquetado actual genera un ejecutable para el entorno utilizado durante la construcción.

Documentación

La documentación técnica se encuentra en la carpeta docs/.
```
Documento	Contenido
00-fundamentos.md	Fundamentos y selección tecnológica
01-widgets.md	Widgets utilizados
02-layouts.md	Layouts y diseño adaptable
03-eventos-async.md	Eventos y asincronía
04-componentes.md	Componentes avanzados y temas
05-arquitectura.md	Arquitectura por capas
06-datos.md	SQLite, Pydantic y API
07-empaquetado.md	Empaquetado y distribución
08-self-review.md	Autoevaluación frente a la rúbrica
```
Principios de diseño

El proyecto sigue los siguientes principios:

* Separación de responsabilidades.
* Bajo acoplamiento.
* Reutilización de componentes.
* Validación de datos.
* Persistencia local.
* Interfaz responsiva.
* Procesamiento asíncrono.
* Diseño adaptable.
* Pruebas automatizadas.
* Documentación técnica.
* Integración continua.

Se evita:

* Lógica de negocio directamente en las vistas.
* Posicionamiento absoluto de componentes.
* Operaciones prolongadas en el hilo de interfaz.
* Estilos duplicados entre componentes.
* Credenciales o secretos almacenados en el código fuente.

Estado del proyecto

Actualmente el proyecto cuenta con:

* Arquitectura por capas.
* Interfaz gráfica PyQt6.
* QTableView.
* Layout adaptable.
* Operaciones asíncronas.
* SQLite.
* Pydantic.
* Integración HTTP.
* Cola offline.
* Sincronización offline.
* Tema claro/oscuro.
* Atajos de teclado.
* Pruebas automatizadas.
* Cobertura superior al 85%.
* GitHub Actions.
* PyInstaller.
* Documentación técnica.
* Instalador nativo.
* Firma y notarización de aplicación macOS.
* Diagrama de arquitectura SVG.
* README final revisado.

Licencia

Este proyecto se desarrolla con fines académicos y demostrativos.