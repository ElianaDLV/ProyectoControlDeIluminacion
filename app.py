from flask import Flask, request, jsonify
from flask_cors import CORS  # Corrige el nombre del módulo
import mysql.connector
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

# Configura tu conexión a la base de datos usando variables de entorno
dbconfig = {
    "host": "bzblpg99biozcrivgozu-mysql.services.clever-cloud.com",
    "user": "uggqczjfkgrrerdg",
    "password": "10SR42jjPz8tnaFfyk6l",
    "database": "bzblpg99biozcrivgozu",
    "port": 3306
}

@app.route("/data", methods=["POST"])
def insertdata():
    if request.is_json:
        data = request.get_json()
        data_to_send = data.get("value")

        if data_to_send is None:
            return jsonify({"status": "error", "message": "data is required"}), 400

        # Aquí va tu lógica para insertar en la base de datos
        try:
            conn = mysql.connector.connect(**dbconfig)  # Corrige el nombre de la variable
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sensor_data (value) VALUES (%s)", (data_to_send,)
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