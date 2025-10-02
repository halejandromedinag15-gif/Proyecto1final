# app.py

import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd

# --- Configuración ---
# Directorio donde se guardarán los archivos cargados
UPLOAD_FOLDER = 'uploads'
# Extensiones de archivo permitidas
ALLOWED_EXTENSIONS = {'csv'} 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegúrate de que el directorio de carga exista al iniciar la app
# Esto evita errores si se borra la carpeta uploads
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

# --- Funciones Auxiliares ---

def allowed_file(filename):
    """Verifica si la extensión del archivo es permitida."""
    # Ej: 'datos.csv' -> ['datos', 'csv'] -> 'csv'
    return '.' in filename and \
filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_csv_for_chart(filepath):
    """
    Función que leerá y preparará los datos del CSV.
    La implementaremos completamente en el Paso 3.
    Por ahora, solo retorna datos de prueba.
    """
    try:
        df = pd.read_csv(filepath)
        # Asumimos que queremos graficar las primeras dos columnas por defecto
        df = df.iloc[:, :2].dropna()
        df.columns = ['label', 'value']

        return {
            'labels': df['label'].tolist(),
            'data': df['value'].tolist(),
            'title': 'Gráfico de Pruebas (Datos reales pronto)'
        }
    except Exception as e:
        print(f"Error procesando CSV en app.py: {e}")
        return None

# --- Rutas de la Aplicación (Manejo del Tráfico Web) ---

@app.route('/') 
@app.route('/index')
def index():
    """Ruta principal: Muestra el formulario de carga."""
    return render_template('index.html') # Busca index.html en la carpeta templates

@app.route('/upload', methods=['POST'])
def upload_file():
    """Maneja la carga del archivo CSV y redirige a la visualización."""
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']

    if file.filename == '' or not allowed_file(file.filename):
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        # Genera una ruta segura y guarda el archivo
        filename = 'uploaded_data.csv' 
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Procesa el archivo y prepara los datos
        chart_data = process_csv_for_chart(filepath)
        
        if chart_data:
            # Pasa los datos procesados a la plantilla de visualización
            return render_template('visualization.html', chart_data=chart_data)
        else:
            return "Error al procesar el archivo CSV. Revise el formato.", 500

# --- Ejecución del Servidor ---
if __name__ == '__main__':
    # El modo debug es útil para que la app se recargue automáticamente al guardar
    app.run(debug=True)