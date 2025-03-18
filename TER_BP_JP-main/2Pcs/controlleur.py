
import socketio

# Création d'un client Socket.IO
sio = socketio.Client()

# Adresse du serveur (remplace par l'IP du Raspberry Pi si nécessaire)
server_url = "http://192.168.228.251:5000"

@sio.event
def connect():
    print("Connecté au serveur!")

@sio.event
def disconnect():
    print("Déconnecté du serveur!")

@sio.on('to_controller')
def handle_message(data):
    print(f"Données reçues: {data}")

try:
    # Connexion au serveur
    sio.connect(server_url)
    print("En attente de données...")
    sio.wait()
except Exception as e:
    print(f"Erreur de connexion: {e}")
