from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os
from datetime import datetime
from zoneinfo import ZoneInfo  # Importar ZoneInfo para manejo de zonas horarias
import pytz

argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')

# Conversión de horario
timestamp = timestamp.replace(tzinfo=pytz.UTC).astimezone(argentina_tz)

app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/*": {"origins": "*"}})

# Configura tu conexión a la base de datos usando variables de entorno
db_config = {
    "host": "bzblpg99biozcrivgozu-mysql.services.clever-cloud.com",
    "user": "uggqczjfkgrrerdg",
    "password": "10SR42jjPz8tnaFfyk6l",
    "database": "bzblpg99biozcrivgozu",
    "port": 3306
}

# Definir la zona horaria de Argentina
argentina_tz = ZoneInfo('America/Argentina/Buenos_Aires')

@app.route("/data", methods=["POST"])
def insert_data():
    if request.is_json:
        data = request.get_json()

        # Extraer los campos necesarios
        light_level = data.get("light_level")  # Este será el campo 'capacidad' en la base de datos
        led_state = data.get("led_state")  # Obtener el estado del LED

        # Comprobar que el campo 'light_level' no sea None y sea un número
        if light_level is None or not isinstance(light_level, (int, float)):
            return jsonify({"status": "error", "message": "light_level es requerido y debe ser un número"}), 400

        # Comprobar que el campo 'led_state' no sea None
        if led_state is None:
            return jsonify({"status": "error", "message": "led_state es requerido"}), 400

        # Conectar a la base de datos e insertar los datos
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insertar datos en la base de datos (omitiendo sensor_id)
            cursor.execute(
                "INSERT INTO capacidad_esp32 (capacidad, estado_led) VALUES (%s, %s)",
                (light_level, led_state)
            )
            conn.commit()
            cursor.close()
            conn.close()
            print("Datos insertados:", {"capacidad": light_level, "estado_led": led_state})  # Log de inserción
            return jsonify({"status": "success"}), 201
        except mysql.connector.Error as err:
            print("Error al insertar datos:", err)  # Log de error
            return jsonify({"status": "error", "message": str(err)}), 500
    else:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

@app.route("/data", methods=["GET"])
def get_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT capacidad, timestamp, estado_led FROM capacidad_esp32 ORDER BY timestamp DESC LIMIT 10")
        rows = cursor.fetchall()
        results = []
        for row in rows:
            capacidad, timestamp, estado_led = row

            # Asegurarse de que timestamp es un objeto datetime
            if isinstance(timestamp, datetime):
                # Asumir que el timestamp está en UTC y convertir a Argentina
                timestamp = timestamp.replace(tzinfo=ZoneInfo('UTC')).astimezone(argentina_tz)
                formatted_date = timestamp.strftime("%d/%m/%Y")  # Formato de fecha
                formatted_time = timestamp.strftime("%H:%M:%S")  # Formato de hora
            else:
                # Manejo en caso de que el timestamp no sea un objeto datetime
                try:
                    timestamp_date = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                    timestamp_date = timestamp_date.replace(tzinfo=ZoneInfo('UTC')).astimezone(argentina_tz)
                    formatted_date = timestamp_date.strftime("%d/%m/%Y")
                    formatted_time = timestamp_date.strftime("%H:%M:%S")
                except:
                    formatted_date = str(timestamp)
                    formatted_time = "00:00:00"  # Valor por defecto

            results.append({
                "capacidad": capacidad,
                "fecha": formatted_date,  # Incluir la fecha en el formato deseado
                "hora": formatted_time,    # Incluir la hora en formato deseado
                "estado_led": estado_led   # Incluir el estado del LED en la respuesta
            })
        cursor.close()
        conn.close()
        print("Datos obtenidos en GET /data:", results)  # Log de obtención de datos
        return jsonify(results), 200
    except mysql.connector.Error as err:
        print("Error al obtener datos en GET /data:", err)  # Log de error
        return jsonify({"status": "error", "message": str(err)}), 500

@app.route("/")
def index():
    print("Accediendo a la ruta principal '/'")
    return send_from_directory(app.static_folder, "index.html")  # Servir el archivo index.html desde la carpeta 'static'

@app.route("/test")
def test_route():
    return "¡El servidor Flask está funcionando correctamente!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Usar el puerto asignado por Render
    app.run(host="0.0.0.0", port=port, debug=True)
