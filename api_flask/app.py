import os
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)  # Corregido _name_ a __name__

# Configura tu conexión a la base de datos usando variables de entorno
db_config = {
    "host": "localhost",  # Asegúrate de que es correcto si MySQL está corriendo localmente.
    "user": "root",  # El usuario de MySQL que creaste.
    "password": "4413",  # La contraseña correcta para ese usuario.
    "database": "mi_base_de_datos"  # El nombre de la base de datos a la que quieres conectarte.
}

@app.route("/data", methods=["POST"])
def insert_data():
    if request.is_json:
        data = request.get_json()
        campo1 = data.get("campo1")
        sensor_id = data.get("sensor_id")  # Opcional

        if campo1 is None:
            return jsonify({"status": "error", "message": "campo1 es requerido"}), 400

        try:
            # Conectar a la base de datos
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insertar datos
            if sensor_id:
                query = "INSERT INTO capacidad_esp32 (capacidad, sensor_id) VALUES (%s, %s)"
                values = (campo1, sensor_id)
            else:
                query = "INSERT INTO capacidad_esp32 (capacidad) VALUES (%s)"
                values = (campo1,)

            cursor.execute(query, values)
            conn.commit()

            cursor.close()
            conn.close()
            return jsonify({"status": "success"}), 201
        except Error as err:
            return jsonify({"status": "error", "message": str(err)}), 500
    else:
        return jsonify({"status": "error", "message": "La solicitud debe ser JSON"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
