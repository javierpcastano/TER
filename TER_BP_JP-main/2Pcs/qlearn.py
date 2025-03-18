import time
import numpy as np
import socketio
import requests

# URL de votre serveur Flask + Socket.IO (remplacez par l'IP de votre serveur).
SERVER_URL = "http://192.168.XX.XX:5000"

sio = socketio.Client()

# Liste des actions possibles pour l'agent Q-learning.
actions = ["DO_NOTHING", "INCREASE_POWER", "DECREASE_POWER"]

# Définition du nombre d'états discrets (par exemple 15, pour 0 à 14 V).
num_states = 15

# Initialisation de la Q-table : q_table[état][action].
q_table = np.zeros((num_states, len(actions)))

# Hyperparamètres Q-learning.
learning_rate = 0.1       # alpha
discount_factor = 0.9     # gamma
epsilon = 0.2            # taux d'exploration

# Plages de vitesse et incrément.
max_speed = 95
min_speed = 0
speed_step = 5
current_speed = 0  # Valeur initiale du duty cycle.

def get_state(voltage):
    """
    Convertit la tension en un état discret entre 0 et num_states - 1.
    Ici, on borne à 14 pour signaler les tensions >= 14 V.
    Adaptez selon votre plage de tension réelle.
    """
    scaled = int(voltage)
    return min(scaled, num_states - 1)

def choose_action(state):
    """
    Sélection de l'action selon la stratégie epsilon-greedy.
    """
    if np.random.rand() < epsilon:
        # Exploration : on choisit une action aléatoire.
        return np.random.choice(len(actions))
    else:
        # Exploitation : on choisit l'action de Q(s,a) la plus élevée.
        return np.argmax(q_table[state])

def update_q_table(state, action, reward, next_state):
    """
    Met à jour la Q-table selon la formule du Q-learning :
    Q(s,a) ← Q(s,a) + α [ R + γ * max_a' Q(s', a') − Q(s,a) ]
    """
    best_next_action = np.argmax(q_table[next_state])
    q_table[state, action] += learning_rate * (
        reward + discount_factor * q_table[next_state, best_next_action]
        - q_table[state, action]
    )

def compute_reward(voltage):
    """
    Fonction de récompense d'exemple :
      - Si la tension >= 14.5, on considère que la voiture est sortie => pénalité forte.
      - Sinon, on récompense la tension la plus élevée possible (< 14.5).
    """
    if voltage >= 14.5:
        # Grosse pénalité si sortie de piste.
        return -15
    else:
        # La récompense augmente à mesure que la tension se rapproche de 14.5 (dans la limite).
        return 10.0 * (voltage / 14.5)

def apply_action(action_idx):
    """
    En fonction de l'action choisie, modifie la variable current_speed
    puis envoie la nouvelle consigne de vitesse au contrôleur (via Socket.IO).
    """
    global current_speed
    action_name = actions[action_idx]

    if action_name == "INCREASE_POWER":
        current_speed += speed_step
    elif action_name == "DECREASE_POWER":
        current_speed -= speed_step
    elif action_name == "DO_NOTHING":
        pass

    # On borne la vitesse entre [min_speed, max_speed].
    current_speed = max(min_speed, min(max_speed, current_speed))

    # Émission d'un événement 'set_speed' : à implémenter côté serveur ou "contrôleur".
    sio.emit('set_speed', {'speed': current_speed})

    print(f"[apply_action] Action: {action_name}, Speed => {current_speed}%")

# ------------------ Gestion des événements Socket.IO --------------------

@sio.event
def connect():
    print("[Q-Learning] Connecté au serveur")

@sio.event
def disconnect():
    print("[Q-Learning] Déconnecté du serveur")

@sio.on('update_plot')
def on_update_plot(data):
    """
    Événement émis par le serveur. 'data' doit contenir 'value' (tension).
    """
    try:
        voltage = data['value']
        print(f"[Q-Learning] Tension reçue: {voltage:.3f} V")

        # Déterminer l'état discret.
        state = get_state(voltage)

        # Choisir une action (epsilon-greedy).
        action_idx = choose_action(state)

        # Appliquer cette action (mise à jour de la vitesse PWM).
        apply_action(action_idx)

        # Calculer la récompense.
        reward = compute_reward(voltage)

        # Dans un enchaînement réaliste, on attendrait la prochaine mesure pour obtenir next_state.
        # Ici, on simplifie en considérant que l'état ne change pas immédiatement.
        next_state = state

        # Mettre à jour la Q-table.
        update_q_table(state, action_idx, reward, next_state)

        print(f"[Q-Learning] Action={actions[action_idx]}, Reward={reward:.2f}")
        print("[Q-Learning] Q-table:\n", q_table)
    except Exception as e:
        print(f"Erreur dans on_update_plot: {e}")

# ------------------------- Lancement -----------------------------------

if __name__ == "__main__":
    try:
        sio.connect(SERVER_URL)
        print("[Q-Learning] En attente des données...")
        sio.wait()
    except KeyboardInterrupt:
        print("[Q-Learning] Interrompu par l'utilisateur.")
    except Exception as e:
        print(f"[Q-Learning] Erreur de connexion : {e}")
