import psycopg2

DB_HOST = "localhost"
DB_NAME = "radar_electoral"
DB_USER = "postgres"
DB_PASS = "admin123"

try:
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()
    
    # Verificamos la base de datos real a la que nos conectamos
    cur.execute("SELECT current_database();")
    print(f"📦 Conectado a la Base de Datos: {cur.fetchone()[0]}")
    
    # Verificamos si la tabla candidatos existe y qué columnas tiene
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='candidatos';
    """)
    columnas = [row[0] for row in cur.fetchall()]
    
    if columnas:
        print(f"✅ Tabla 'candidatos' encontrada. Columnas actuales:\n{columnas}")
        if 'total_receitas' in columnas:
            print("\n🎉 ¡La columna 'total_receitas' SÍ existe en esta base de datos!")
        else:
            print("\n❌ ¡ALERTA! La columna 'total_receitas' NO existe en esta base de datos. Por eso fallaba el script.")
    else:
        print("❌ La tabla 'candidatos' NO existe en esta base de datos o el esquema está vacío.")
        
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Error de conexión: {e}")