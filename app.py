from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'host': 'tu_host',
    'database': 'mi_base_de_datos'
}

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        # Obtener los datos enviados desde el ESP32
        data = request.get_json()
        
        # Extraer los valores del JSON
        light_level = data.get('light_level')
        sensor_id = data.get('sensor_id')
        timestamp = data.get('timestamp')
        estado_led = data.get('estado_led')  # Nuevo campo

        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Inserción de los datos en la tabla
        insert_query = '''
        INSERT INTO capacidad_esp32 (capacidad, timestamp, sensor_id, estado_led)
        VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (light_level, timestamp, sensor_id, estado_led))
        conn.commit()

        # Cerrar la conexión
        cursor.close()
        conn.close()

        return jsonify({'message': 'Datos recibidos correctamente!'}), 201

    except Exception as e:
        print('Error al recibir datos:', e)
        return jsonify({'error': 'Error al recibir datos'}), 500

@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Consulta para obtener los datos
        select_query = "SELECT capacidad, timestamp, sensor_id, estado_led FROM capacidad_esp32 ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(select_query)

        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return jsonify({
                'capacidad': result[0],
                'timestamp': result[1].isoformat(),  # Convertir a ISO 8601 para facilitar el manejo en el cliente
                'sensor_id': result[2],
                'estado_led': result[3]
            }), 200
        else:
            return jsonify({'error': 'No hay datos disponibles'}), 404

    except Exception as e:
        print('Error al obtener datos:', e)
        return jsonify({'error': 'Error al obtener datos'}), 500

if __name__ == '__main__':
    app.run(debug=True)
