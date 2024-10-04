# Proyecto Control De Iluminación Automático 

## Descripción
Este proyecto tiene como objetivo escalar una plataforma IoT basada en microcontroladores ESP32, ampliando su funcionalidad desde una simple capa física hasta una infraestructura completa que incluye una capa de transporte de datos y un sistema de almacenamiento en una base de datos MySQL. Los dispositivos ESP32 recopilan datos de sensores de luz (LDR) y controlan actuadores (LED), transmitiendo la información a través de WiFi a un backend desarrollado con Flask, que a su vez almacena los datos en MySQL para su análisis y monitoreo en tiempo real.

## Tecnologías utilizadas

### Hardware:
ESP32: Microcontrolador.
Sensor de Luz LDR: Sensor de luz.
LED: Actuador.
Pantalla OLED SSD1306: Display para visualización.

### Software:
MicroPython: Lenguaje de programación para ESP32.
Flask: Framework de Python para el backend.
MySQL: Sistema de gestión de bases de datos.
Wokwi: Plataforma de simulación para ESP32.
