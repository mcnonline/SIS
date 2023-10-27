# FLASK +IO temporário por @mcnonline #Aprendendo a desenvolver 1.0
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import sqlite3

# Caminho dos certificados e chaves de teste
#CERT_PATH = 'C:\\Users\\mcnon\\OneDrive\\Área de Trabalho\\SIS ROOMS\\.cert\\server.crt'
#KEY_PATH = 'C:\\Users\\mcnon\\OneDrive\\Área de Trabalho\\SIS ROOMS\\.cert\\server.key'

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app, certfile='C:\\Users\\mcnon\\OneDrive\\Área de Trabalho\\SIS ROOMS\\.cert\\server.key', keyfile='C:\\Users\\mcnon\\OneDrive\\Área de Trabalho\\SIS ROOMS\\.cert\\server.key')

def iniciar_banco_de_dados():
    conn = sqlite3.connect('rooms.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
                 id INTEGER PRIMARY KEY,
                 room_number INTEGER,
                 status TEXT
                 )''')

    for room_number in range(1, 6):
        cursor.execute("INSERT OR IGNORE INTO rooms (room_number, status) VALUES (?, ?)", (room_number, 'vazio'))

    for room_number in range(11, 18):
        cursor.execute("INSERT OR IGNORE INTO rooms (room_number, status) VALUES (?, ?)", (room_number, 'vazio'))

    for room_number in range(21, 28):
        cursor.execute("INSERT OR IGNORE INTO rooms (room_number, status) VALUES (?, ?)", (room_number, 'vazio'))

    for room_number in range(31, 38):
        cursor.execute("INSERT OR IGNORE INTO rooms (room_number, status) VALUES (?, ?)", (room_number, 'vazio'))

    conn.commit()
    conn.close()

def atualizar_status_quarto(room_number, status):
    conn = sqlite3.connect('rooms.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE rooms SET status = ? WHERE room_number = ?", (status, room_number))
    conn.commit()
    conn.close()

    socketio.emit('atualizacao_status', {'roomNumber': room_number, 'status': status})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sis')
def sis():
    return render_template('gerenciamento_quartos.html')

@app.route('/atualizar_status', methods=['POST'])
def atualizar_status():
    data = request.json
    room_number = data['roomNumber']
    status = data['status']
    atualizar_status_quarto(room_number, status)
    return 'Status atualizado com sucesso'

@socketio.on('connect')
def connect():
    conn = sqlite3.connect('rooms.db')
    cursor = conn.cursor()
    cursor.execute("SELECT room_number, status FROM rooms")
    rooms = cursor.fetchall()
    conn.close()

    for room in rooms:
        emit('atualizacao_status', {'roomNumber': room[0], 'status': room[1]})
    
    print("Cliente conectado ao servidor Socket.IO")  
  
@socketio.on('atualizacao_status')
def handle_status_update(data):
    room_number = data['roomNumber']
    status = data['status']
    atualizar_status_quarto(room_number, status)

    print("Status atualizado para o quarto {room_number}: {status}")

    emit('atualizacao_status', {'roomNumber': room_number, 'status': status}, broadcast=True)
        
if __name__ == '__main__':
    iniciar_banco_de_dados()
    socketio.run(app, host='0.0.0.0', port=443)