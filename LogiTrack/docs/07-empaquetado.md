07 — Empaquetado y distribución

Objetivo

LogiTrack Desktop utiliza PyInstaller para generar una versión ejecutable de la aplicación que no requiere iniciar el programa mediante el intérprete de Python.

El empaquetado permite distribuir la aplicación de escritorio de forma independiente del entorno de desarrollo y constituye una etapa necesaria para preparar el proyecto para su instalación en equipos de usuario final.

⸻

1. Herramienta utilizada

La herramienta seleccionada para el empaquetado es:

PyInstaller

La dependencia se instala dentro del entorno virtual del proyecto mediante:
```
python -m pip install pyinstaller
```
La versión utilizada durante el desarrollo fue:

PyInstaller 6.22.3

El entorno utilizado corresponde a:

Python 3.12.14
macOS arm64

⸻

2. Archivo de configuración

La configuración de PyInstaller se encuentra en:
```
scripts/build.spec
```
El archivo define como punto de entrada:
```
logitrack/__main__.py
```
y establece el nombre del ejecutable:

LogiTrack

También se configura:

console=False

Esto permite que la aplicación gráfica se ejecute sin abrir una consola adicional.

⸻

3. Proceso de compilación

El ejecutable se genera desde la raíz del proyecto mediante:
```
python -m PyInstaller --clean scripts/build.spec
```
La opción --clean permite eliminar archivos temporales y cachés anteriores antes de realizar la compilación.

El proceso genera los directorios de trabajo de PyInstaller y el ejecutable final dentro de:

dist/

⸻

4. Ejecutable generado

En el entorno de desarrollo utilizado, PyInstaller generó:

dist/LogiTrack

El archivo resultante tiene un tamaño aproximado de:

34 MB

El ejecutable fue probado directamente desde la terminal:
```
./dist/LogiTrack
```
La aplicación inició correctamente y mostró la interfaz gráfica de LogiTrack Desktop.

⸻

5. Validación del ejecutable

La validación realizada después del empaquetado comprobó que:

* El ejecutable puede iniciarse sin utilizar python -m logitrack.
* La ventana principal de LogiTrack Desktop se muestra correctamente.
* PyQt6 está incluido en el paquete generado.
* La aplicación puede recibir interacción del usuario.
* La aplicación puede cerrarse normalmente.

Esta prueba permite comprobar que el resultado del empaquetado es ejecutable fuera del flujo habitual de desarrollo.

⸻

6. Consideraciones de plataforma

El ejecutable fue generado en:

macOS
Apple Silicon / arm64

Por lo tanto, este artefacto está orientado al entorno utilizado durante el desarrollo.

Para distribuir LogiTrack Desktop en Windows o Linux sería necesario generar los ejecutables correspondientes desde cada plataforma o mediante un sistema de compilación compatible.

PyInstaller no genera de forma general un único ejecutable universal para todos los sistemas operativos.

⸻

7. Flujo de distribución

El flujo actual es:
```
Código fuente
     ↓
PyInstaller
     ↓
scripts/build.spec
     ↓
dist/LogiTrack
     ↓
Prueba del ejecutable
     ↓
Distribución
```
Este proceso permite separar el entorno de desarrollo del artefacto que será utilizado por el usuario final.

⸻

8. Mejoras futuras

Como evolución del proyecto se puede incorporar:

* Generación de un paquete .app nativo para macOS.
* Creación de un instalador para Windows.
* Firma de código.
* Notarización para macOS.
* Automatización del build mediante GitHub Actions.
* Generación automática de artefactos por versión.
* Publicación de releases.
* Instalador nativo.

Estas funcionalidades no son necesarias para el funcionamiento actual del ejecutable, pero representan posibles mejoras para una distribución profesional.

⸻

9. Resultado

La implementación actual demuestra que LogiTrack Desktop puede ser empaquetado como un ejecutable independiente mediante PyInstaller.

El ejecutable fue generado correctamente y probado en el equipo de desarrollo, donde la aplicación inició y mostró la interfaz gráfica sin necesidad de ejecutar manualmente el módulo Python.