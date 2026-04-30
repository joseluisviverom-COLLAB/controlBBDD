from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Base de datos temporal (Se guarda mientras el servicio esté activo)
cursos_db = []

@app.route('/cursos/', methods=['GET'])
def get_cursos():
    return jsonify(cursos_db)

@app.route('/cursos/', methods=['POST'])
def add_curso():
    try:
        datos = request.json
        # Verificación básica de que recibimos datos
        if not datos or 'titulo' not in datos:
            return jsonify({"error": "Datos incompletos"}), 400
            
        cursos_db.append(datos)
        print(f"✅ Curso registrado en la API: {datos['titulo']}")
        return jsonify({"mensaje": "Guardado exitosamente", "curso": datos}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import os
    # Render asigna el puerto automáticamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    return {"mensaje": "Curso guardado con éxito", "id": nuevo_curso.id}
