import os
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configura tu conexión a la base de datos usando variables de entorno
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),  # Reemplaza "localhost" si es necesario
    "user": os.getenv("DB_USER", "tu_usuario"),
    "password": os.getenv("DB_PASSWORD", "tu_contraseña"),
    "database": os.getenv("DB_NAME", "amt"),
}

@app.route("/data", methods=["POST"])
def insert_data():
    if request.is_json:
        data = request.get_json()
        capacidad = data.get("campo1")  # Asegúrate de que el campo en el JSON se llama "campo1"
        sensor_id = data.get("sensor_id")  # Opcional, si envías este dato

        if capacidad is None:
            return jsonify({"status": "error", "message": "campo1 es requerido"}), 400

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            if sensor_id:
                cursor.execute(
                    "INSERT INTO capacidad_esp32 (capacidad, sensor_id) VALUES (%s, %s)",
                    (capacidad, sensor_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO capacidad_esp32 (capacidad) VALUES (%s)", (capacidad,)
                )
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"status": "success"}), 201
        except mysql.connector.Error as err:
            return jsonify({"status": "error", "message": str(err)}), 500
    else:
        return jsonify({"status": "error", "message": "La solicitud debe ser JSON"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
