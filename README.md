# SIGUEPOP 🚗💨

<p align="justify">
<strong>SIGUEPOP</strong> es una aplicación de escritorio desarrollada en Python para configurar y enviar parámetros de control a un robot siguelíneas basado en ESP32.
</p>

<p align="justify">
La aplicación permite ajustar constantes de control, guardar la configuración localmente y enviar los datos al microcontrolador mediante comunicación <strong>Bluetooth Serial SPP</strong>.
</p>

---

## Descripción del proyecto

<p align="justify">
Este proyecto nace como una herramienta sencilla para facilitar la calibración de un robot siguelíneas sin tener que modificar y recompilar el firmware cada vez que se quieran cambiar los parámetros de control.
</p>

<p align="justify">
Desde la interfaz gráfica se pueden modificar valores como las constantes PID, la velocidad base, el umbral de detección y otros parámetros del comportamiento del robot. Al pulsar el botón de envío, la aplicación manda los datos al ESP32 en formato JSON a través de un puerto COM Bluetooth.
</p>

## Interfaz de la aplicación

![Interfaz de SIGUEPOP](img/FOTO_APP.png)

---

## Funcionalidades principales

* Interfaz gráfica de escritorio con **CustomTkinter**.
* Comunicación con ESP32 mediante **Bluetooth Serial SPP**.
* Búsqueda automática de puertos Bluetooth disponibles.
* Selección manual del puerto COM.
* Envío de parámetros en formato JSON.
* Recepción de respuesta del ESP32.
* Timeout de seguridad: si el ESP32 no responde en 4 segundos, la conexión se cierra.
* Guardado de configuración en un archivo `config.json`.
* Terminal integrada para visualizar logs de conexión, envío y respuesta.
* Icono personalizado para la aplicación.

---

## Parámetros configurables

<p align="justify">
La aplicación permite modificar y enviar los siguientes parámetros:
</p>

| Parámetro   | Descripción                                       |
| ----------- | ------------------------------------------------- |
| `KP`        | Ganancia proporcional del controlador             |
| `KI`        | Ganancia integral del controlador                 |
| `KD`        | Ganancia derivativa del controlador               |
| `Kv`        | Parámetro adicional asociado a velocidad          |
| `Kvi`       | Parámetro adicional asociado a velocidad/integral |
| `Vbase`     | Velocidad base del robot                          |
| `Volantazo` | Intensidad de giro o corrección brusca            |
| `Umbral`    | Umbral de detección de línea                      |
| `COM`       | Elegir el puerto COM                              |
| `BAUDRATE`  | Velocidad de comunicación serie                   |

---

## Tecnologías utilizadas

* Python
* CustomTkinter
* Tkinter
* PySerial
* JSON
* Bluetooth Serial SPP
* ESP32

---
