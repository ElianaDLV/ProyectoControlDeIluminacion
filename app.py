from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os
from datetime import datetime  # Importar datetime

app = Flask(__name__, static_folder='static')  # Asegúrate de tener una carpeta 'static'
CORS(app, resources={r"/*": {"origins": "*"}})

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
            return jsonify({"status": "success"}), 201
        except mysql.connector.Error as err:
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
        print("Datos obtenidos:", results)  # Log de los datos obtenidos
        return jsonify(results), 200
    except mysql.connector.Error as err:
        print("Error al obtener datos:", err)  # Log de error
        return jsonify({"status": "error", "message": str(err)}), 500

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
