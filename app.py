from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os
from datetime import datetime  # Importar datetime

app = Flask(__name__, static_folder='static')  # Especificar la carpeta estática
CORS(app, resources={r"/*": {"origins": "*"}})  # Habilitar CORS para todos los orígenes

# Configura tu conexión a la base de datos usando variables de entorno
db_config = {
    "host": "bzblpg99biozcrivgozu-mysql.services.clever-cloud.com",
    "user": "uggqczjfkgrrerdg",
    "password": "10SR42jjPz8tnaFfyk6l",
    "database": "bzblpg99biozcrivgozu",
    "port": 3306
}

@app.route("/data", methods=["POST"])
def insert_data():
    if request.is_json:
        data = request.get_json()

        # Extraer los campos necesarios
        light_level = data.get("light_level")  # Este será el campo 'capacidad' en la base de datos
        sensor_id = data.get("sensor_id", "ESP32_Sensor")  # Puedes ajustar esto según tus necesidades

        # Comprobar que el campo 'light_level' no sea None y sea un número
        if light_level is None or not isinstance(light_level, (int, float)):
            return jsonify({"status": "error", "message": "light_level es requerido y debe ser un número"}), 400

        # Conectar a la base de datos e insertar los datos
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Omitimos el campo 'timestamp' en la consulta para que MySQL lo genere automáticamente
            cursor.execute(
                "INSERT INTO capacidad_esp32 (capacidad, sensor_id) VALUES (%s, %s)",
                (light_level, sensor_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            print("Datos insertados:", {"capacidad": light_level, "sensor_id": sensor_id})  # Log de inserción
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
        cursor.execute("SELECT capacidad, timestamp, sensor_id FROM capacidad_esp32 ORDER BY timestamp DESC LIMIT 10")
        rows = cursor.fetchall()
        results = []
        for row in rows:
            capacidad, timestamp, sensor_id = row
            # Convertir timestamp a formato ISO
            if isinstance(timestamp, datetime):
                timestamp = timestamp.isoformat()
            else:
                timestamp = str(timestamp)  # Asegurarse de que sea una cadena
            results.append({
                "capacidad": capacidad,
                "timestamp": timestamp,
                "sensor_id": sensor_id
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
