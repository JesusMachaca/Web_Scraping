import os
from flask import Flask, render_template, request
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

@app.route('/', methods=['GET', 'POST'])
def index():
    # Obtención de filtros desde el formulario
    selected_empresa = request.form.get('empresa', '').lower()
    selected_tipo_jornada = request.form.get('tipo_jornada', '').lower()
    
    # Conexión a la base de datos
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Consulta base con condiciones dinámicas
        query = """
            SELECT titulo, empresa, ubicacion, requerimientos, enlace, tipo_jornada 
            FROM ofertas_laborales 
            WHERE 
                (lower(titulo) LIKE '%pre%' OR lower(requerimientos) LIKE '%estudiante%')
                AND lower(requerimientos) LIKE '%sistemas%'
        """
        filters = []
        
        # Aplicar filtros de empresa y tipo_jornada si están presentes
        if selected_empresa:
            query += " AND lower(empresa) = %s"
            filters.append(selected_empresa)
        if selected_tipo_jornada:
            query += " AND lower(tipo_jornada) = %s"
            filters.append(selected_tipo_jornada)
        
        # Ejecutar la consulta con los filtros
        cursor.execute(query, filters)
        
        # Almacenar resultados en una lista de diccionarios
        job_listings = [dict(row) for row in cursor.fetchall()]
        
        # Obtener valores únicos para los campos de filtrado
        cursor.execute("SELECT DISTINCT lower(empresa) FROM ofertas_laborales")
        empresas = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT lower(tipo_jornada) FROM ofertas_laborales")
        tipo_jornadas = [row[0] for row in cursor.fetchall()]
        
    except Exception as e:
        print("Error al conectar con la base de datos o al ejecutar la consulta:", e)
        job_listings = []
        empresas = []
        tipo_jornadas = []
        
    finally:
        # Cerrar conexión
        cursor.close()
        connection.close()
    
    # Renderizar plantilla HTML con los datos
    return render_template(
        'index.html', 
        job_listings=job_listings, 
        empresas=empresas, 
        tipo_jornadas=tipo_jornadas,
        selected_empresa=selected_empresa,
        selected_tipo_jornada=selected_tipo_jornada
    )

# Iniciar la aplicación
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
