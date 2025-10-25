
from flask import Flask, render_template, request, jsonify
import logging
import os
from process import process, u_list

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Создаем папки для изображений если их нет
os.makedirs('static/images', exist_ok=True)

@app.route('/')
def main():
    return render_template('index.html',
                         initial_equations=u_list,
                         faks=["S", "F", "G", "T", "A", "D", "I", "P", "C"],
                         equations=[
                             "F1s", "F1x8", "F2s", "F2x8", "F2x1", "F2x7", "F3x8", "F3x1", "F3x7", "F4x8",
                             "F4x7", "F4x1", "F5s", "F5x1", "F5x7", "F6s", "F6x8", "F7x1", "F8s", "F8x4",
                             "F9s", "F9x1", "F9x7", "F10s", "F10x1", "F10x7", "F11s", "F11x6", "F12x11"
                         ])

@app.route('/initial_equations')
def get_initial_equations():
    return jsonify(u_list)

@app.route('/draw_graphics', methods=['POST'])
def draw_graphics():
    try:
        data = request.get_json()
        process(data["initial_equations"], data["faks"], data["equations"], data["restrictions"])
        return jsonify({"status": "Выполнено"})
    except Exception as e:
        logging.error(f"Error in draw_graphics: {e}")
        return jsonify({"status": "Ошибка"})

@app.route('/graphic')
def get_graphic():
    return render_template('graphic.html')

@app.route('/diagrams')
def get_diagrams():
    return render_template('diagrams.html')
@app.route('/facks')
def get_disturbances():
    return render_template('facks.html')

if __name__ == '__main__':
    # For local testing only; on PythonAnywhere, WSGI will import app
    app.run(host='0.0.0.0', port=5000, debug=True)