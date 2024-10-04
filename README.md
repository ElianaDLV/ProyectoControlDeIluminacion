![Miniatura IVR (1)](https://github.com/user-attachments/assets/0290406f-7b30-4855-a57c-80bfd41d62fe)

### Link a wokwi
https://wokwi.com/projects/410672224127161345

## 📋 Descripción
Este proyecto tiene como objetivo escalar una plataforma IoT basada en microcontroladores ESP32, ampliando su funcionalidad desde una simple capa física hasta una infraestructura completa que incluye una capa de transporte de datos y un sistema de almacenamiento en una base de datos MySQL. Los dispositivos ESP32 recopilan datos de sensores de luz (LDR) y controlan actuadores (LED), transmitiendo la información a través de WiFi a un backend desarrollado con Flask, que a su vez almacena los datos en MySQL para su análisis y monitoreo en tiempo real.

## 💻 Tecnologías utilizadas

### Hardware:
ESP32: Microcontrolador.<br />
Sensor de Luz LDR: Sensor de luz.<br />
LED: Actuador.<br />
Pantalla OLED SSD1306: Display para visualización.<br />

### Software:
MicroPython: Lenguaje de programación para ESP32.<br />
Flask: Framework de Python para el backend.<br />
MySQL: Sistema de gestión de bases de datos.<br />
Wokwi: Plataforma de simulación para ESP32.<br />

## ⚙️ Requisitos previos de software
Python 3.8+ – Para el backend.<br />
pip – Gestor de paquetes de Python.<br />
Git – Para clonar el repositorio.<br />
MicroPython – Firmware para ESP32.<br />
VS Code (opcional) – Editor de código recomendado.<br />
Acceso a un servidor para alojar el backend (puede ser local o en la nube).<br />
