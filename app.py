import os
from flask import Flask, render_template
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# Configuración de conexión a la base de datos PostgreSQL
DB_CONFIG = {
    'dbname': 'bd_ofertas',
    'user': 'user',
    'password': 'i3QtlW963o6QQtlWfqAEB2O5b14vBdQq',
    'host': 'dpg-csls2l1u0jms73d1c72g-a.oregon-postgres.render.com',
    'port': '5432'
}

@app.route('/')
def index():
    # Conexión a la base de datos
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Consulta SQL para recuperar datos de la tabla Ofertas
        query = "SELECT titulo, empresa, ubicacion, requerimientos, enlace FROM ofertas_laborales where titulo like '%pre%'"
        cursor.execute(query)
        
        # Almacenar resultados en una lista de diccionarios
        job_listings = [dict(row) for row in cursor.fetchall()]
        
    except Exception as e:
        print("Error al conectar con la base de datos o al ejecutar la consulta:", e)
        job_listings = []
        
    finally:
        # Cerrar conexión
        cursor.close()
        connection.close()
    
    # Renderizar plantilla HTML con los datos
    return render_template('index.html', job_listings=job_listings)

# Iniciar la aplicación
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
