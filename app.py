from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir solicitudes de diferentes orígenes

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
        capacidad = data.get("light_level")  # Cambia esto por el valor que desees enviar como capacidad
        sensor_id = data.get("sensor_id")  # Este campo puede ser opcional o puedes definirlo en el ESP32
        timestamp = data.get("timestamp")  # También puedes usar el timestamp actual si no se envía

        # Comprobar que el campo 'capacidad' no sea None
        if capacidad is None:
            return jsonify({"status": "error", "message": "capacidad es requerido"}), 400

        # Conectar a la base de datos e insertar los datos
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO capacidad_esp32 (capacidad, timestamp, sensor_id) VALUES (%s, %s, %s)",
                (capacidad, timestamp, sensor_id)  # Ajusta según tu estructura de tabla
            )
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"status": "success"}), 201
        except mysql.connector.Error as err:
            return jsonify({"status": "error", "message": str(err)}), 500
    else:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
