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
    selected_empresa = request.form.get('empresa', '').strip().lower()
    selected_tipo_jornada = request.form.get('tipo_jornada', '').strip().lower()
    
    # Conexión a la base de datos
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Base de consulta
        query = """
            SELECT titulo, empresa, ubicacion, requerimientos, enlace, tipo_jornada 
            FROM ofertas_laborales 
            WHERE 
                (lower(titulo) LIKE '%pre%' OR lower(requerimientos) LIKE '%estudiante%')
                AND lower(requerimientos) LIKE '%sistemas%'
        """
        filters = []

        # Caso 1: Sin filtros (Ambos en "Todas")
        if not selected_empresa and not selected_tipo_jornada:
            cursor.execute(query)
        
        # Caso 2: Solo filtro de empresa
        elif selected_empresa and not selected_tipo_jornada:
            query += " AND lower(empresa) = %s"
            filters.append(selected_empresa)
            cursor.execute(query, filters)
        
        # Caso 3: Solo filtro de tipo_jornada
        elif not selected_empresa and selected_tipo_jornada:
            query += " AND lower(tipo_jornada) = %s"
            filters.append(selected_tipo_jornada)
            cursor.execute(query, filters)
        
        # Caso 4: Ambos filtros activos
        elif selected_empresa and selected_tipo_jornada:
            query += " AND lower(empresa) = %s AND lower(tipo_jornada) = %s"
            filters.extend([selected_empresa, selected_tipo_jornada])
            cursor.execute(query, filters)
        
        # Obtener resultados de la consulta
        job_listings = [dict(row) for row in cursor.fetchall()]

        # Consulta para obtener opciones únicas de los filtros
        cursor.execute("SELECT DISTINCT lower(empresa) FROM ofertas_laborales WHERE empresa IS NOT NULL")
        empresas = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT lower(tipo_jornada) FROM ofertas_laborales WHERE tipo_jornada IS NOT NULL")
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
