from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import time 

app = Flask(__name__)
socketio = SocketIO(app)  


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No JSON data received'}), 400
        #Données envoyes par le capteur
        value = data.get('value', None)
        timestamp = data.get('timestamp',None)

        if value is not None and timestamp is not None: 
            #print(f"Received value: {value}")  
            #Envoyer au Raspberry pi 
            socketio.emit('update_plot',  {'value': value})
            #socketio.emit('update_plot', {'value':value, 'timestamp': timestamp})
            return jsonify({'status': 'success'})
        else:
            #print("Invalid data received")  
            return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    except Exception as e:
        #print(f"Error: {e}")  
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)

