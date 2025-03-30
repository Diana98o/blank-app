import streamlit as st

import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# Conectar a la base de datos
conn = sqlite3.connect("tareas.db")
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        tarea TEXT,
        estado TEXT,
        fecha TEXT
    )
''')
conn.commit()

st.title("📌 Gestor de Tareas con Base de Datos")

# Entrada de datos
nombre = st.text_input("Escribe tu nombre:")
tarea = st.text_input("Describe tu tarea:")
estado = st.selectbox("Estado de la tarea:", ["Pendiente", "En progreso", "Completada"])
fecha = st.date_input("Fecha de la tarea:", date.today())

# Guardar tarea en la base de datos
if st.button("Guardar tarea"):
    cursor.execute("INSERT INTO tareas (nombre, tarea, estado, fecha) VALUES (?, ?, ?, ?)",
                   (nombre, tarea, estado, fecha))
    conn.commit()
    st.success("✅ ¡Tarea guardada con éxito!")

# Mostrar las tareas guardadas
st.subheader("📋 Tareas Guardadas")
cursor.execute("SELECT * FROM tareas")
tareas = cursor.fetchall()

if tareas:
    df = pd.DataFrame(tareas, columns=["ID", "Nombre", "Tarea", "Estado", "Fecha"])
    st.dataframe(df)

    # Exportar a Excel
    excel_file = "tareas.xlsx"
    df.to_excel(excel_file, index=False)

    # Botón de descarga
    with open(excel_file, "rb") as f:
        st.download_button("📥 Descargar Excel", f, file_name=excel_file, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

else:
    st.write("⚠️ No hay tareas registradas.")

# Cerrar la conexión con la base de datos