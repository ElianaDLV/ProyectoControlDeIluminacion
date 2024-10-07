![Miniatura IVR (1)](https://github.com/user-attachments/assets/0290406f-7b30-4855-a57c-80bfd41d62fe)

### Links para ver su función
### Simulación en Wokwi
Puedes ver y ejecutar la simulación en Wokwi y, ver la interfaz mediante los siguientes enlaces:
- [Simulación en Wokwi](https://wokwi.com/projects/410672224127161345)
- [Sitio en Render](https://proyectocontroldeiluminacion.onrender.com/)  

## 📋 Descripción
Este proyecto tiene como objetivo escalar una plataforma IoT basada en microcontroladores ESP32, ampliando su funcionalidad desde una simple capa física hasta una infraestructura completa que incluye una capa de transporte de datos y un sistema de almacenamiento en una base de datos MySQL. Los dispositivos ESP32 recopilan datos de sensores de luz (LDR) y controlan actuadores (LED), transmitiendo la información a través de WiFi a un backend desarrollado con Flask, que a su vez almacena los datos en MySQL para su análisis y monitoreo en tiempo real.
La interfaz web ha sido mejorada para ofrecer una experiencia de usuario más atractiva y moderna, con un tema oscuro acentuado en tonos violetas y lilas.

## 💻 Tecnologías utilizadas

### Hardware:
- **ESP32**: Microcontrolador.
- **Sensor de Luz LDR**: Sensor de luz.
- **LED**: Actuador.
- **Pantalla OLED SSD1306**: Display para visualización.

### Software:
- **MicroPython**: Lenguaje de programación para ESP32.
- **Flask**: Framework de Python para el backend.
- **MySQL**: Sistema de gestión de bases de datos.
- **Wokwi**: Plataforma de simulación para ESP32.
- **Bootstrap**: Framework CSS para diseño responsivo y estilizado.
- **Chart.js**: Biblioteca JavaScript para gráficos interactivos.
- **Font Awesome**: Biblioteca de iconos para mejorar la interfaz.

## 🛠️ Características
- **Interfaz Web Moderna**: Diseño de tema oscuro con acentos en tonos violetas y lilas.
- **Monitoreo en Tiempo Real**: Visualización en tiempo real del nivel de luz y estado del LED.
- **Gráficos Interactivos**: Historial de datos de nivel de luz representados en gráficos dinámicos.
- **Tarjetas Informativas**: Visualización destacada de la última lectura de nivel de luz y el estado actual del LED con iconos.
- **API RESTful**: Endpoints para insertar y obtener datos desde el backend Flask.
- **Base de Datos Escalable**: Almacenamiento eficiente de datos en MySQL.

## 🚀 Instalación

### Requisitos Previos
- **Python 3.8+**
- **MySQL Server**
- **ESP32 con MicroPython**

### Backend (Flask)
1. Clona el repositorio:
    ```bash
    git clone https://github.com/ElianaDLV/ProyectoControlDeIluminacion.git
    cd ProyectoControlDeIluminacion
    ```

2. Crea y activa un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Configura las variables de entorno para la base de datos en un archivo `.env` o directamente en `app.py`.

5. Inicia el servidor Flask:
    ```bash
    python app.py
    ```
