Fase 3 — Layouts y geometría responsive

Objetivo

Diseñar una interfaz de escritorio adaptable que mantenga una distribución funcional al cambiar el tamaño de la ventana, evitando el uso de coordenadas absolutas.

Layouts utilizados

LogiTrack Desktop utiliza los siguientes administradores de geometría de PyQt6:

* QVBoxLayout: organiza verticalmente las secciones principales de la ventana.
* QHBoxLayout: organiza horizontalmente elementos como el encabezado y los controles.
* QFormLayout: organiza las etiquetas y campos del formulario de registro.
* QSplitter: permite modificar dinámicamente la proporción de espacio entre la tabla de envíos y el formulario.

No se utilizan posiciones absolutas mediante move(), setGeometry() ni coordenadas manuales.

Distribución principal

La ventana utiliza una estructura vertical:
```
Ventana principal
│
├── Encabezado
│   ├── LogiTrack Desktop
│   └── Gestión de envíos
│
└── Área de contenido
    │
    └── QSplitter horizontal
        ├── Tabla de envíos
        └── Formulario de nuevo envío
```
El QSplitter permite que el usuario modifique la distribución horizontal de la interfaz.

Políticas de tamaño

La tabla utiliza una política de tamaño expansible:
```
QSizePolicy.Policy.Expanding
```
Esto permite que aproveche el espacio disponible cuando la ventana aumenta de tamaño.

El formulario mantiene un rango de ancho mediante:
```
form_group.setMinimumWidth(300)
form_group.setMaximumWidth(400)
```
De esta manera se evita que el formulario ocupe una proporción excesiva de la pantalla.

Encabezado

El encabezado se encuentra dentro de un QWidget con una política vertical fija:
```
header_widget.setSizePolicy(
    QSizePolicy.Policy.Expanding,
    QSizePolicy.Policy.Fixed,
)
```
Esto evita que el encabezado crezca innecesariamente cuando la ventana se maximiza.

Pruebas realizadas

Se realizaron pruebas en tres escenarios:

Ventana pequeña

Se verificó que los elementos permanecieran visibles y que no existieran superposiciones.

Resultado: Correcto.

Ventana mediana

Se verificó la distribución entre la tabla y el formulario.

Resultado: Correcto.

Ventana maximizada

Se verificó que el espacio adicional fuera aprovechado principalmente por la tabla y que el encabezado mantuviera una altura compacta.

Resultado: Correcto.

Prueba del divisor

También se probó el divisor del QSplitter, comprobando que el usuario puede modificar manualmente la proporción entre la tabla y el formulario.

Resultado: Correcto.

Conclusión

La interfaz cumple con el objetivo de utilizar layouts administrados por Qt y adaptarse a diferentes tamaños de ventana sin depender de posiciones absolutas.

Esta implementación proporciona una base adecuada para continuar con eventos, señales y operaciones asíncronas en las siguientes fases del proyecto.