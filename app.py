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
        campo1 = data.get("campo1")
        humidity = data.get("humidity")
        light_level = data.get("light_level")
        led_state = data.get("led_state")
        timestamp = data.get("timestamp")

        # Comprobar que el campo 'campo1' no sea None
        if campo1 is None:
            return jsonify({"status": "error", "message": "campo1 es requerido"}), 400

        # Conectar a la base de datos e insertar los datos
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sensor_data (temperature, humidity, light_level, led_state, timestamp) VALUES (%s, %s, %s, %s, %s)",
                (campo1, humidity, light_level, led_state, timestamp)
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
