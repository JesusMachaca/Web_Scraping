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

# Ruta principal para mostrar las ofertas de trabajo
@app.route('/')
def index():
    # Conexión a la base de datos
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Consulta SQL para recuperar datos de la tabla Ofertas
        query = "SELECT titulo, empresa, ubicacion, requerimientos FROM Ofertas"
        cursor.execute(query)
        
        # Almacenar resultados en una lista de diccionarios
        job_listings = [dict(row) for row in cursor.fetchall()]
        
    except Exception as e:
        print("Error al conectar con la base de datos:", e)
        job_listings = []
        
    finally:
        # Cerrar conexión
        cursor.close()
        connection.close()
    
    # Renderizar plantilla HTML con los datos
    return render_template('index.html', job_listings=job_listings)

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
