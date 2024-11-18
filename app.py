from flask import Flask, render_template, request, jsonify, session
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar sesiones

# URL de LM Studio para las interacciones de chat
LM_STUDIO_URL = "http://host.docker.internal:1234/v1/chat/completions"

# Configuración para el tamaño máximo de contenido permitido
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024  # 64 MB

# Ruta principal que muestra la página del chatbot
@app.route('/')
def index():
    # Inicializar el historial de conversación si no existe en la sesión
    if 'conversation' not in session:
        session['conversation'] = []
    return render_template('index.html')

# Ruta para manejar las interacciones del chatbot
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('user_message')
    
    if not user_message:
        return jsonify({'response': 'No se proporcionó mensaje de usuario.'}), 400

    # Agregar el mensaje del usuario al historial de conversación
    session['conversation'].append({"role": "user", "content": user_message})
    
    # Preparar el payload con el historial completo
    payload = {
        "messages": session['conversation'],
        "max_tokens": 200,
        "temperature": 0.7
    }

    try:
        # Solicitud POST a LM Studio
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=300)
        response.raise_for_status()

        # Obtener la respuesta de LM Studio y agregarla al historial
        llm_response = response.json().get('choices', [{}])[0].get('message', {}).get('content', "Respuesta vacía del modelo.")
        session['conversation'].append({"role": "assistant", "content": llm_response})

    except requests.exceptions.RequestException as e:
        llm_response = f"Error de conexión con LM Studio: {e}"

    except ValueError as e:
        llm_response = "Error al procesar la respuesta de LM Studio."

    # Retorna la respuesta al frontend
    return jsonify({'response': llm_response})

# Ruta para limpiar el historial de conversación (opcional)
@app.route('/reset', methods=['POST'])
def reset_conversation():
    session['conversation'] = []
    return jsonify({'response': 'Conversación reiniciada.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
