# TER_BP_JP

## Commandes utilisées frequemment

Copier des fichiers qui sont dans le raspberry:
scp pi@your_raspberry_ip:/path/to/remote/file /path/to/local/destination

Lancer les scripts pythons en arriere-plan:
nohup python3 script.py > output.log 2>&1 &

Arreter le script precedent:
kill $(pgrep -f script.py)

Verifier le fonctionnement de systemd-networkd:
sudo systemctl enable systemd-networkd
sudo systemctl restart systemd-networkd
sudo systemctl status systemd-networkd

Hostnames et users des Raspberrys:
capteur@kpteur
pi@controlleur
