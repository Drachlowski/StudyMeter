# StudyMeter

## 1. Anforderungen

Zum Ausführen der Backend-Applikation wird Docker oder Python3 mit den installierten requirements benötigt


## 2. Einrichtung mit Docker
1. [Docker](https://www.docker.com/products/docker-desktop/) downloaden
2. Docker installieren
    - Bei Installation bietet es sich an, bei Configuration "Use WSL 2 instead of Hyper-V" anzukreuzen
    - Bei Abschluss PC neustarten (hier wird WSL installiert)
3. Zur Sicherheit WSL Updaten
    - Powershell öffnen
    - Den Command "wsl --update" eingeben
4. Docker Desktop starten (für den Fall, dass es auf einem Windows ausgeführt wird)
5. Poweshell im Ordner öffnen, wo sich das compose.yaml befindet und in der Poweshell "docker-compose up" eingeben
6. That's it, auf das Backend kann dann mit http://localhost:8000/ zugegriffen werden



