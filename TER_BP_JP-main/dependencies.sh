#!/bin/bash

usage() {
    echo "  -u, --update   Mettre à jour et upgrader les paquets système avant l'installation."
    exit 1
}

UPDATE_SYSTEM=false
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -u|--update) UPDATE_SYSTEM=true ;;
        -h|--help) usage ;;
        *) echo "Option inconnue : $1"; usage ;;
    esac
    shift
done

if [ "$UPDATE_SYSTEM" = true ]; then
    echo "Mise à jour des paquets système..."
    sudo apt update && sudo apt upgrade -y
else
    echo "Mise à jour du système ignorée."
fi

read -p "Entrez le nom de l'environnement virtuel à créer : " env_name

echo "Vérification de Python3..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 non trouvé. Installation de Python3..."
    sudo apt install python3 -y
else
    echo "Python3 est déjà installé."
fi

echo "Vérification de pip3..."
if ! command -v pip3 &> /dev/null; then
    echo "pip3 non trouvé. Installation de pip3..."
    sudo apt install python3-pip -y
else
    echo "pip3 est déjà installé."
fi

echo "Vérification de virtualenv..."
if ! pip3 show virtualenv &> /dev/null; then
    echo "virtualenv non trouvé. Installation de virtualenv..."
    sudo apt install python3-virtualenv
else
    echo "virtualenv est déjà installé."
fi

echo "Création de l'environnement virtuel '$env_name'..."
python3 -m venv "$env_name"

echo "Activation de l'environnement virtuel..."
source "$env_name/bin/activate"

echo "Installation des dépendances Python..."
pip install requests flask flask_socketio RPi.GPIO adafruit-blinka adafruit-ads1x15

